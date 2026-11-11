import { readdir, readFile, access } from 'node:fs/promises';
import { resolve, relative, dirname, basename } from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseFrontmatter, parseExerciseYaml } from '../src/content-format.ts';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const errors = [];
const lessons = new Map();
const exercises = new Map();
const references = new Map();
async function files(dir) {
  const found = [];
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    const path = resolve(dir, entry.name);
    if (entry.isDirectory()) found.push(...await files(path));
    else found.push(path);
  }
  return found.sort();
}
function check(condition, message) { if (!condition) errors.push(message); }
function text(value) { return typeof value === 'string' && value.trim().length > 0; }

for (const path of await files(resolve(root, 'content/exercises'))) {
  if (basename(path) !== 'exercise.yml') continue;
  const location = relative(root, path);
  try {
    const item = parseExerciseYaml(await readFile(path, 'utf8'));
    check(text(item.id) && !exercises.has(item.id), `${location}: missing or duplicate ID`);
    check(basename(dirname(path)) === item.id, `${location}: folder must match exercise ID`);
    check(text(item.title) && text(item.prompt), `${location}: title and prompt are required`);
    check(Number.isInteger(item.part) && item.part >= 1 && item.part <= 3, `${location}: invalid part`);
    check(['mcq', 'python'].includes(item.type), `${location}: unsupported type`);
    if (item.type === 'mcq') {
      check(typeof item.multiple === 'boolean', `${location}: multiple must be true or false`);
      check(Array.isArray(item.options) && item.options.length >= 2, `${location}: at least two options required`);
      const options = item.options ?? [];
      check(new Set(options.map(option => option.id)).size === options.length, `${location}: duplicate option IDs`);
      for (const option of options) {
        check(text(option.id) && text(option.text) && text(option.explanation) && typeof option.correct === 'boolean', `${location}: incomplete option`);
      }
      const correct = options.filter(option => option.correct).length;
      check(item.multiple ? correct >= 1 : correct === 1, `${location}: incorrect answer configuration`);
    } else if (item.type === 'python') {
      for (const name of ['starter.py', 'tests.py', 'solution.py']) {
        try { await access(resolve(dirname(path), name)); }
        catch { errors.push(`${location}: missing ${name}`); }
      }
    }
    exercises.set(item.id, item);
  } catch (error) { errors.push(`${location}: ${error.message}`); }
}

for (const path of await files(resolve(root, 'content/lessons'))) {
  if (!path.endsWith('.md')) continue;
  const location = relative(root, path);
  try {
    const { metadata, body } = parseFrontmatter(await readFile(path, 'utf8'));
    check(text(metadata.id) && !lessons.has(metadata.id), `${location}: missing or duplicate ID`);
    check(text(metadata.title) && Number.isInteger(metadata.order), `${location}: title and integer order required`);
    check(Number.isInteger(metadata.part) && metadata.part >= 1 && metadata.part <= 3, `${location}: invalid part`);
    check(!/<(?:Exercise|Editor|CodeStepper|ChapterDiagramGenerator|LearningObjectives|InfoBox)\b/.test(body), `${location}: platform component remains`);
    const fences = body.match(/^\s*```/gm) ?? [];
    check(fences.length % 2 === 0, `${location}: unbalanced code fences`);
    for (const match of body.matchAll(/^:::exercise\s+(\S+)\s*$/gm)) {
      const id = match[1];
      check(exercises.has(id), `${location}: unknown exercise ${id}`);
      check(exercises.get(id)?.part === metadata.part, `${location}: exercise ${id} belongs to another part`);
      references.set(id, (references.get(id) ?? 0) + 1);
    }
    lessons.set(metadata.id, { ...metadata, body, location });
  } catch (error) { errors.push(`${location}: ${error.message}`); }
}
for (const [id] of exercises) check(references.get(id) === 1, `${id}: expected one lesson reference, found ${references.get(id) ?? 0}`);
for (const lesson of lessons.values()) {
  for (const match of lesson.body.matchAll(/\]\(#\/([^)?#]+)(?:\?[^)]*)?\)/g)) {
    check(lessons.has(match[1]), `${lesson.location}: unknown lesson link ${match[1]}`);
  }
}
const counts = { lessons: lessons.size, mcq: [...exercises.values()].filter(e => e.type === 'mcq').length, python: [...exercises.values()].filter(e => e.type === 'python').length };
if (process.argv.includes('--snapshot')) {
  for (const [name, expected] of Object.entries({ lessons: 26, mcq: 70, python: 73 })) {
    check(counts[name] === expected, `Workshop snapshot: expected ${expected} ${name}, found ${counts[name]}`);
  }
}
if (errors.length) {
  console.error(errors.join('\n'));
  process.exitCode = 1;
} else console.log(`Content valid: ${counts.lessons} lessons, ${counts.mcq} MCQs, ${counts.python} Python exercises.`);
