/** Node-only verification using the exact Python harness shipped to browsers. */
import { readFile, readdir, mkdir, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { Worker, isMainThread, parentPort } from 'node:worker_threads';
import assert from 'node:assert/strict';
import { parse } from 'yaml';

const root = fileURLToPath(new URL('../', import.meta.url));
const read = (file) => readFile(path.join(root, file), 'utf8');

if (!isMainThread) {
  const { loadPyodide } = await import('pyodide');
  const python = await loadPyodide();
  python.FS.writeFile('/home/pyodide/workshop_support.py', await read('src/python/workshop_support.py'));
  await python.runPythonAsync(await read('src/python/harness.py'));
  const execute = python.globals.get('workshop_execute');
  parentPort.on('message', ({ id, code, input, tests }) => {
    try {
      parentPort.postMessage({ id, result: JSON.parse(tests === undefined
        ? execute(code, input) : execute(code, input, tests)) });
    } catch (error) {
      parentPort.postMessage({ id, result: { stdout: '', stderr: String(error), error: String(error) } });
    }
  });
  parentPort.postMessage({ ready: true });
} else {
  class Runner {
    worker = null;
    nextId = 0;
    async run(code, input = '', tests) {
      if (!this.worker) {
        const worker = new Worker(new URL(import.meta.url));
        this.worker = worker;
        await new Promise((resolve, reject) => {
          const timer = setTimeout(() => reject(new Error('Python initialization timed out')), 60_000);
          worker.once('error', (error) => { clearTimeout(timer); reject(error); });
          worker.once('message', (message) => { clearTimeout(timer); assert.ok(message.ready); resolve(); });
        });
      }
      const worker = this.worker;
      const id = ++this.nextId;
      return new Promise((resolve) => {
        const timer = setTimeout(() => {
          worker.terminate();
          this.worker = null;
          resolve({ stdout: '', stderr: '', error: 'Execution timed out', timedOut: true });
        }, 10_000);
        worker.once('message', (message) => {
          clearTimeout(timer);
          assert.equal(message.id, id);
          resolve(message.result);
        });
        worker.postMessage({ id, code, input, tests });
      });
    }
    close() { this.worker?.terminate(); }
  }

  const runner = new Runner();
  const snapshot = process.argv.includes('--snapshot');
  const report = {
    runtime: 'Pyodide 314.0.7',
    mode: snapshot ? 'original-snapshot' : 'current-content',
    regressionScope: snapshot ? 'runtime and original-exercise variants' : 'runtime only; original-exercise variants excluded',
    references: [], starters: [], regressions: [],
  };
  let failed = 0;
  try {
    const directories = await readdir(path.join(root, 'content/exercises'));
    const exercises = [];
    for (const id of directories) {
      const folder = `content/exercises/${id}`;
      const meta = parse(await read(`${folder}/exercise.yml`));
      if (meta.type !== 'python') continue;
      exercises.push({ ...meta, folder, tests: await read(`${folder}/tests.py`), solution: await read(`${folder}/solution.py`), starter: await read(`${folder}/starter.py`) });
    }
    for (const exercise of exercises) {
      const reference = await runner.run(exercise.solution, '', exercise.tests);
      report.references.push({ id: exercise.id, title: exercise.title, passed: reference.passed === true, checks: reference.tests?.length ?? 0, ...(!reference.passed && { result: reference }) });
      if (!reference.passed) {
        failed++;
        console.error(`FAIL reference: ${exercise.title}`, JSON.stringify(reference));
      }
      const starter = await runner.run(exercise.starter, '', exercise.tests);
      const rejected = starter.passed !== true;
      report.starters.push({ id: exercise.id, title: exercise.title, rejected, timedOut: !!starter.timedOut });
      if (!rejected) {
        failed++;
        console.error(`FAIL starter unexpectedly passes: ${exercise.title}`);
      }
      if (report.references.length % 10 === 0) console.log(`Verified ${report.references.length}/${exercises.length} references and starters`);
    }

    async function scenario(name, check) {
      try {
        await check();
        report.regressions.push({ name, passed: true });
      } catch (error) {
        failed++;
        report.regressions.push({ name, passed: false, error: String(error) });
        console.error(`FAIL scenario: ${name}`, error.message);
      }
    }
    await scenario('Blank, Unicode, and final input without newline', async () => {
      const result = await runner.run('first = input()\nsecond = input()\nprint(repr(first))\nprint(second.upper())', '\nä');
      assert.equal(result.stdout, "''\nÄ\n");
      assert.equal(result.stderr, '');
    });
    await scenario('Exhausted input gives actionable feedback', async () => {
      const result = await runner.run('input()');
      assert.match(result.error, /more input/);
      assert.match(result.stderr, /EOFError/);
    });
    await scenario('Syntax errors retain source locations', async () => {
      const result = await runner.run('print(');
      assert.match(result.stderr, /SyntaxError/);
      assert.match(result.stderr, /main.py/);
    });
    await scenario('Output is bounded', async () => {
      const result = await runner.run('print("x" * 200000)');
      assert.ok(result.stdout.length < 101_000);
      assert.match(result.stdout, /truncated/);
    });
    await scenario('Builtins, working directory, and globals do not leak', async () => {
      await runner.run('import builtins, os\nbuiltins.input = lambda *args: "leaked"\nos.chdir("/")\nsecret = 123');
      const result = await runner.run('print(input())\nprint("secret" in globals())', 'fresh');
      assert.equal(result.stdout, 'fresh\nFalse\n');
    });
    await scenario('Infinite execution is terminated and the next run recovers', async () => {
      const result = await runner.run('while True:\n    pass');
      assert.ok(result.timedOut);
      assert.equal((await runner.run('print("recovered")')).stdout, 'recovered\n');
    });

    // These fixtures deliberately describe the original course snapshot.
    // Participant edits should only be judged by their own current checks.
    if (snapshot) {
      const byTitle = (part) => {
        const found = exercises.find((e) => e.title.toLowerCase().includes(part));
        assert.ok(found, `Missing regression fixture: ${part}`);
        return found;
      };
      async function rejectedVariant(title, code) {
        const exercise = byTitle(title);
        const result = await runner.run(code, '', exercise.tests);
        assert.notEqual(result.passed, true);
        assert.ok(result.tests?.some((test) => !test.passed), JSON.stringify(result));
      }
      await scenario('An alternate correct output implementation is accepted', async () => {
        const exercise = byTitle('welcome card');
        assert.equal((await runner.run('print("********\\nWelcome!\\n********")', '', exercise.tests)).passed, true);
      });
      await scenario('Extra output is rejected', () => rejectedVariant('welcome card', byTitle('welcome card').solution + '\nprint("extra")'));
      await scenario('Reading all messages before printing is rejected', () => rejectedVariant('five-message announcer', 'messages = [input() for _ in range(5)]\nfor number, message in enumerate(messages, 1):\n    print(f"MESSAGE {number}: {message.upper()}")'));
      await scenario('Archive state mutation is rejected despite correct output', () => rejectedVariant('search archive titles', 'titles = [input() for _ in range(int(input()))]\nterm = input()\ntitles[:] = [title for title in titles if term.lower() in title.lower()]\nmatching_titles = titles\nprint(f"Matches: {matching_titles}")'));
      await scenario('Mutating a supplied list is rejected', () => rejectedVariant('record another reading', 'def with_reading_added(readings, reading):\n    readings.append(reading)\n    return readings'));
      await scenario('Required direct iteration is checked', () => rejectedVariant('count all vowels', 'word = input().strip().lower()\nprint(sum(word.count(vowel) for vowel in "aeiou"))'));
      await scenario('Rounding a function result is rejected', () => rejectedVariant('estimate a delivery route', 'def route_cost(distance, rate):\n    return round(distance * rate, 2)'));
    }

    await mkdir(path.join(root, '.qa'), { recursive: true });
    const reportFile = snapshot ? '.qa/grading-snapshot-results.json' : '.qa/grading-results.json';
    await writeFile(path.join(root, reportFile), JSON.stringify(report, null, 2) + '\n');
    console.log(`${report.references.filter((r) => r.passed).length}/${report.references.length} reference solutions pass; ${report.starters.filter((r) => r.rejected).length}/${report.starters.length} starters rejected; ${report.regressions.filter((r) => r.passed).length}/${report.regressions.length} ${snapshot ? 'snapshot' : 'runtime-only'} regression scenarios pass.`);
    process.exitCode = failed ? 1 : 0;
  } finally {
    runner.close();
  }
}
