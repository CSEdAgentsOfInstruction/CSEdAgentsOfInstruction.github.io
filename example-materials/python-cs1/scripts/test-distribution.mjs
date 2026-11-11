/** Maintainer acceptance test: install and edit a clean source ZIP, then serve
 * its production build beneath a nested URL. Never changes the source course. */
import assert from 'node:assert/strict';
import { mkdtemp, mkdir, readFile, writeFile, stat, rm } from 'node:fs/promises';
import { resolve, dirname, extname, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import { tmpdir } from 'node:os';
import { createServer } from 'node:http';
import { spawn, spawnSync } from 'node:child_process';
import { chromium } from '@playwright/test';
import { unzipSync } from 'fflate';
import { parse, stringify } from 'yaml';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const temporary = await mkdtemp(resolve(tmpdir(), 'python-workshop-'));
const unpacked = resolve(temporary, 'folder with spaces');
const npmCli = process.env.npm_execpath;
if (!npmCli && process.platform === 'win32') throw new Error('Run this task with npm run test:distribution.');
const npm = npmCli ? process.execPath : 'npm';
const npmArguments = npmCli ? [npmCli] : [];
const cacheIndex = process.argv.indexOf('--cache');
const cacheArguments = cacheIndex >= 0 ? ['--cache', process.argv[cacheIndex + 1]] : [];
const welcome = '55da8386-276f-429b-a161-4b77422a198a';
const single = '45696958-a59c-4479-8188-f7fb9ac70e67';
let browser, dev, server;
const report = { cleanInstall: false, nestedProduction: false, sourceReloads: [], externalRequests: [] };

function command(args, cwd) {
  const result = spawnSync(npm, [...npmArguments, ...args], { cwd, encoding: 'utf8', timeout: 120_000, env: process.env });
  if (result.error) throw result.error;
  if (result.status !== 0) throw new Error(`npm ${args.join(' ')} failed:\n${result.stdout}\n${result.stderr}`);
  console.log(`npm ${args.join(' ')} passed in isolated source ZIP.`);
}
async function availablePort() {
  const probe = createServer();
  await new Promise(resolve => probe.listen(0, '127.0.0.1', resolve));
  const port = probe.address().port;
  await new Promise(resolve => probe.close(resolve));
  return port;
}
async function waitForServer(url) {
  const deadline = Date.now() + 30_000;
  while (Date.now() < deadline) {
    try { if ((await fetch(url)).ok) return; } catch {}
    await new Promise(resolve => setTimeout(resolve, 150));
  }
  throw new Error(`Server did not start: ${url}`);
}
async function hasText(locator, text) {
  await locator.filter({ hasText: text }).first().waitFor({ state: 'visible', timeout: 20_000 });
}
async function setCode(page, card, code) {
  const editor = card.getByTestId('code-input');
  await editor.click();
  await editor.press('ControlOrMeta+A');
  await page.keyboard.insertText(code);
}

try {
  const entries = unzipSync(new Uint8Array(await readFile(resolve(root, '../python-cs1.zip'))));
  for (const [name, contents] of Object.entries(entries)) {
    assert.ok(name.startsWith('python-cs1/') && !name.split('/').includes('..'), `Unsafe archive member: ${name}`);
    assert.ok(!/(^|\/)(introcs|node_modules|\.git|\.env|\.qa)(\/|$)/.test(name), `Unexpected archive member: ${name}`);
    const target = resolve(unpacked, name);
    await mkdir(dirname(target), { recursive: true });
    await writeFile(target, contents);
  }
  const project = resolve(unpacked, 'python-cs1');
  command(['ci', ...(process.argv.includes('--offline') ? ['--offline'] : []), ...cacheArguments], project);
  command(['run', 'build'], project);
  report.cleanInstall = true;

  const output = resolve(project, 'dist');
  const prefix = '/workshop/course/';
  server = createServer(async (request, response) => {
    try {
      const pathname = decodeURIComponent(new URL(request.url, 'http://localhost').pathname);
      if (!pathname.startsWith(prefix)) { response.writeHead(404).end(); return; }
      const target = resolve(output, pathname.slice(prefix.length) || 'index.html');
      if (!target.startsWith(output + sep) || !(await stat(target)).isFile()) { response.writeHead(404).end(); return; }
      const types = { '.html': 'text/html', '.js': 'application/javascript', '.mjs': 'application/javascript', '.css': 'text/css', '.wasm': 'application/wasm', '.json': 'application/json', '.zip': 'application/zip' };
      response.writeHead(200, { 'Content-Type': types[extname(target)] ?? 'application/octet-stream' });
      response.end(await readFile(target));
    } catch { response.writeHead(404).end(); }
  });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const origin = `http://127.0.0.1:${server.address().port}`;
  browser = await chromium.launch();
  const context = await browser.newContext();
  context.on('request', request => {
    if (/^https?:/.test(request.url()) && new URL(request.url()).origin !== origin) report.externalRequests.push(request.url());
  });
  const page = await context.newPage();
  await page.goto(`${origin}${prefix}#/part-1/3-talking-with-a-program`);
  await page.reload();
  const card = page.locator(`[data-exercise="${welcome}"]`);
  await card.waitFor();
  await setCode(page, card, await readFile(resolve(project, `content/exercises/${welcome}/solution.py`), 'utf8'));
  await card.getByRole('button', { name: /^Check / }).click();
  await card.locator('.completion-badge').waitFor({ state: 'visible', timeout: 30_000 });
  assert.deepEqual(report.externalRequests, [], 'The production course must not request external runtime services');
  report.nestedProduction = true;
  await mkdir(resolve(root, '.qa'), { recursive: true });
  await card.screenshot({ path: resolve(root, '.qa/distribution-nested.png') });
  await context.close();

  const devPort = await availablePort();
  dev = spawn(npm, [...npmArguments, 'run', 'dev', '--', '--port', String(devPort), '--strictPort'], { cwd: project, stdio: 'pipe', env: process.env });
  let serverLog = '';
  dev.stdout.on('data', chunk => { serverLog += chunk; });
  dev.stderr.on('data', chunk => { serverLog += chunk; });
  const devUrl = `http://127.0.0.1:${devPort}/`;
  await waitForServer(devUrl).catch(error => { throw new Error(`${error.message}\n${serverLog}`); });
  const live = await browser.newPage();
  await live.goto(`${devUrl}#/part-1/3-talking-with-a-program`);
  const lessonPath = resolve(project, 'content/lessons/part-1/3-talking-with-a-program.md');
  await writeFile(lessonPath, (await readFile(lessonPath, 'utf8')) + '\n\nWorkshop lesson edit appears here.\n');
  await hasText(live.locator('.markdown p'), 'Workshop lesson edit appears here.');
  report.sourceReloads.push('lesson Markdown');

  const liveCard = live.locator(`[data-exercise="${welcome}"]`);
  await setCode(live, liveCard, 'print("saved workshop draft")');
  const starterPath = resolve(project, `content/exercises/${welcome}/starter.py`);
  await writeFile(starterPath, 'print("updated source starter")\n');
  await liveCard.locator('.starter-notice').waitFor({ state: 'visible' });
  await liveCard.getByRole('button', { name: 'Load updated starter', exact: true }).click();
  await hasText(liveCard.getByTestId('code-input'), 'updated source starter');
  report.sourceReloads.push('starter Python and saved-draft reconciliation');

  const checksPath = resolve(project, `content/exercises/${welcome}/tests.py`);
  const checksReloaded = live.waitForEvent('load', { timeout: 20_000 });
  await writeFile(checksPath, (await readFile(checksPath, 'utf8')) + '\nclass WorkshopChangedCheck(unittest.TestCase):\n    def test_edited_check(self):\n        self.fail("Workshop edited test marker")\n');
  await checksReloaded;
  await liveCard.getByRole('button', { name: /^Check / }).click();
  await hasText(liveCard.locator('.execution-output'), 'Workshop edited test marker');
  report.sourceReloads.push('Python checks');

  const mcqPath = resolve(project, `content/exercises/${single}/exercise.yml`);
  const mcq = parse(await readFile(mcqPath, 'utf8'));
  mcq.prompt = 'Workshop MCQ edit appears here.';
  await writeFile(mcqPath, stringify(mcq));
  await live.goto(`${devUrl}#/part-1/2-programs-and-the-programming-workflow`);
  await hasText(live.locator(`[data-exercise="${single}"]`), mcq.prompt);
  report.sourceReloads.push('MCQ YAML');

  const newId = '00000000-0000-4000-8000-000000000001';
  await mkdir(resolve(project, `content/exercises/${newId}`));
  await writeFile(resolve(project, `content/exercises/${newId}/exercise.yml`), stringify({ ...mcq, id: newId, title: 'A newly added workshop question' }));
  const workflow = resolve(project, 'content/lessons/part-1/2-programs-and-the-programming-workflow.md');
  await writeFile(workflow, (await readFile(workflow, 'utf8')) + `\n\n:::exercise ${newId}\n`);
  await live.locator(`[data-exercise="${newId}"]`).waitFor({ state: 'visible', timeout: 20_000 });
  report.sourceReloads.push('new exercise discovery');
  console.log(JSON.stringify(report, null, 2));
  await writeFile(resolve(root, '.qa/distribution-results.json'), JSON.stringify(report, null, 2) + '\n');
} finally {
  await browser?.close();
  if (dev) { dev.kill('SIGTERM'); await new Promise(resolve => dev.once('close', resolve)); }
  if (server) await new Promise(resolve => server.close(resolve));
  await rm(temporary, { recursive: true, force: true });
}
