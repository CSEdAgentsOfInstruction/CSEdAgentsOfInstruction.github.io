import { readdir, readFile, writeFile, mkdir, cp, rm } from 'node:fs/promises';
import { resolve, dirname, relative } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
import { zipSync } from 'fflate';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const parent = dirname(root);
const demo = resolve(parent, 'python-demo');
const archive = resolve(parent, 'python-cs1.zip');
const npmCli = process.env.npm_execpath;
if (!npmCli && process.platform === 'win32') throw new Error('Run this task with npm run package.');
const command = npmCli ? process.execPath : 'npm';
const result = spawnSync(command, [...(npmCli ? [npmCli] : []), 'run', 'build'], { cwd: root, stdio: 'inherit' });
if (result.error) throw result.error;
if (result.status !== 0) process.exit(result.status ?? 1);

// Preserve the license texts of both shipped and build-time dependencies.
const lock = JSON.parse(await readFile(resolve(root, 'package-lock.json'), 'utf8'));
let notices = 'Third-party dependencies\nGenerated from the pinned package-lock.json. Each dependency retains its own license.\n';
for (const [path, dependency] of Object.entries(lock.packages)) {
  if (!path.startsWith('node_modules/')) continue;
  const directory = resolve(root, path);
  const names = await readdir(directory).catch(error => {
    if (error.code === 'ENOENT') return null; // Optional packages for other operating systems.
    throw error;
  });
  if (!names) continue;
  notices += `\n\n${path.replace(/^node_modules\//, '')} ${dependency.version}\nLicense: ${dependency.license ?? 'See package notice'}\n`;
  for (const name of names) {
    if (/^(licen[cs]e|copying|notice)(\..*)?$/i.test(name)) {
      const contents = await readFile(resolve(directory, name), 'utf8').catch(() => null);
      if (contents) notices += `\n${name}\n${contents}\n`;
    }
  }
}
await writeFile(resolve(root, 'THIRD-PARTY-NOTICES.txt'), notices);

// Only this dedicated generated output is replaced; never traverse the private platform.
await mkdir(demo, { recursive: true });
const previous = await readdir(demo);
if (previous.length && !previous.includes('WORKSHOP-DEMO.txt')) {
  throw new Error(`Refusing to overwrite an unrecognized directory: ${demo}`);
}
for (const name of previous) await rm(resolve(demo, name), { recursive: true, force: true });
await cp(resolve(root, 'dist'), demo, { recursive: true });
await writeFile(resolve(demo, 'WORKSHOP-DEMO.txt'), 'Generated from ../python-cs1 with npm run package. Edit the source app, not this directory.\n');
await writeFile(resolve(demo, 'THIRD-PARTY-NOTICES.txt'), notices);
await cp(resolve(root, 'CONTENT-NOTICE.txt'), resolve(demo, 'CONTENT-NOTICE.txt'));
await cp(resolve(root, 'NOTICE.md'), resolve(demo, 'NOTICE.txt'));

const members = {};
async function include(path) {
  const absolute = resolve(root, path);
  const entries = await readdir(absolute, { withFileTypes: true }).catch(() => null);
  if (entries) {
    for (const entry of entries) {
      if (['.DS_Store', '__pycache__'].includes(entry.name) || entry.name.endsWith('.pyc')) continue;
      if (entry.isSymbolicLink()) throw new Error(`Source archives cannot include symlinks: ${path}/${entry.name}`);
      await include(`${path}/${entry.name}`);
    }
  } else members[`python-cs1/${path}`] = new Uint8Array(await readFile(absolute));
}
for (const path of [
  '.gitignore', '.nvmrc', 'package.json', 'package-lock.json', 'tsconfig.json',
  'vite.config.mjs', 'playwright.config.ts', 'index.html', 'README.md', 'AUTHORING.md',
  'NOTICE.md', 'CONTENT-NOTICE.txt', 'THIRD-PARTY-NOTICES.txt', 'extraction-manifest.json',
  'content', 'src', 'scripts', 'tests',
]) await include(path);
await writeFile(archive, zipSync(members, { level: 6 }));
console.log(`Demo: ${relative(root, demo)}\nSource ZIP: ${relative(root, archive)} (${Object.keys(members).length} files)`);
