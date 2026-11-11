/** One-time, explicit extraction. Never used by dev/build. Existing Python files
 * are preserved so rerunning cannot overwrite subsequently ported grading. */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import vm from 'node:vm';
import { parse, stringify } from 'yaml';

const destination = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const source = process.argv[2] && path.resolve(process.argv[2]);
if (!source) throw new Error('Usage: node scripts/extract-content.mjs /path/to/introcs');
const assignments = path.join(source, 'opencs-assignment-repository/introduction-to-programming');
const materials = path.join(source, 'opencs-materials/courses/en/introduction-to-programming');
const registry = new Map();
const manifest = {
  edition: 'current English introduction-to-programming',
  omittedChapters: ['part-1/8-decisions-and-games', 'part-2/8-repetition-and-games', 'part-3/10-functions-and-games'],
  lessons: [], exercises: [], omitted: [], solutionsMissingInSource: [],
};
for (const relative of fs.readdirSync(assignments, { recursive: true }).sort()) {
  if (!/\.ya?ml$/.test(relative)) continue;
  const filename = path.join(assignments, relative);
  const data = parse(fs.readFileSync(filename, 'utf8'));
  function index(value, parent = null) {
    if (!value || typeof value !== 'object') return;
    if (value.uuid) registry.set(value.uuid, { data: value, filename, relative, parent });
    for (const item of Object.values(value)) {
      if (Array.isArray(item)) item.forEach((child) => index(child, value));
      else if (item && typeof item === 'object') index(item, value);
    }
  }
  index(data);
}
const seen = new Set();
function adaptProse(text, id) {
  const removedLeadIns = [
    'You will see exercises where you arrange steps written in plain language.',
    'A first, smaller version of the study-time idea is simply to accumulate minutes',
    'The same conversation can be described in plain language first. Arrange',
    'A small program often stores more than one named value. The next exercise',
    'Now try the same kind of translation in plain language. Arrange',
    'The final exercise combines input, state changes, branch order, boundaries, and output. Use the rubric',
    'Arrange the blocks of a short program before writing your own loop.',
    'You can also describe the same loop in plain language. Arrange',
    'The following exercise asks you to explain a related indexed loop',
    'In the next exercise, explain what happens to the list',
    'Practise that pattern in plain language. Most of the program is given',
    'Build the same kind of counter in plain language for reading-session lengths.',
    'A single loop can update more than one result. Trace each variable separately, then explain',
    'Try calling a function in natural language. Assemble',
    "Finally, explain the chapter's central distinction in your own words:",
    "Now try writing a function's missing step in natural language.",
    'Trace a call to another function with more than one `return` statement:',
    'Finish by explaining how printed output and returned values follow different paths:',
    'Finish by explaining why mutation and reassignment have different effects:',
    'The program below is incomplete - the function is missing its counting step.',
    'Write two functions from scratch in natural language, then call them',
    'Then review and explain another generated implementation:',
    'Trace several focused conversion handlers before combining one with a loop:',
    'Trace how arguments are bound to parameters in several calls:',
    'Trace reassignment, mutation, and aliasing side by side:',
    'In the next exercise, a console stores a transmission as a string.',
    'Trace a few definitions and calls before writing your own:',
    'Trace displayed and returned values:',
    'Now trace the changes yourself. For each assignment, first evaluate',
  ];
  text = text.split('\n\n').filter((paragraph) => !removedLeadIns.some((prefix) => paragraph.trim().startsWith(prefix))).join('\n\n');
  const replacements = [
    ['The code stepper below demonstrates the process.', 'The example below demonstrates the process. Trace how the values change, then run it to check your prediction.'],
    ['Step through the program below. Before clicking Next, predict which part of the list or program state will change.', 'Trace the program below on paper. Before each statement, predict which part of the list or program state will change.'],
    ['The stepper shows the two lists separately.', 'Keep separate records of the two lists as you trace this example.'],
    ['In the stepper, predict which indexed cell will be highlighted after each assignment.', 'Predict the value at each index after each assignment, then run the program to check the final list.'],
    ['Step through the two calls and watch the state panel.', 'Trace the two calls, writing down the local names and their values.'],
    ['Step through the same program. Watch when `answer` gets its value and when output appears.', 'Trace the same program. Notice when `answer` gets its value and when output appears.'],
    ['Step through the same program. Compare what is printed with the value assigned to `result`.', 'Trace the same program. Compare what is printed with the value assigned to `result`.'],
    ['Step through the call.', 'Trace the call.'],
    ['Step through the same loop with two fixed inputs: `hello`, then `42`. Watch `text` in the state panel to see each response. The walkthrough leaves out the `Integer: ` prompts; its output panel shows the messages from `print`.', 'Enter `hello` and `42` on separate lines in the input box before running this example. Trace how `text` changes after each input. The expected output below shows only the messages from `print`; Run also displays the `Integer: ` prompts.'],
    ['If you run the program, type `Ada`, and press Enter, Python receives the text `Ada`. Nothing is stored yet, so the program cannot use the answer later. The program simply ends after the user presses Enter.', 'In this workshop app, type `Ada` in the input box before pressing **Run**. Python reads that line when it reaches `input(...)`. Nothing is stored yet, so the program cannot use the answer later. For programs with several inputs, enter each answer on its own line before running.'],
    ["> The output window shows the prompt and the text you typed. The text you typed is shown in blue, but it is not program output. It is the user's input. The program does not print your answer; it only receives it.", '> Your answers remain in the input box. The output area shows what the program prints, including any prompts passed to `input(...)`. Reading an answer does not automatically print it. If the program needs more lines than you provided, add them to the input box and run again.'],
    ['If the user types `Ada`, the interactive terminal transcript normally looks like this:', 'In an interactive terminal, entering `Ada` would normally produce this transcript:'],
    ['The first line contains the prompt from `input(...)` followed by the text the user typed. The second line is program output produced by `print(name)`.', 'The first line of that terminal transcript contains the prompt followed by the typed answer. The second line is output from `print(name)`. In this app, input and output are separate: with `Ada` in the input box, the output area shows `What is your name? Ada` on one line, because the prompt has no newline and only `print(name)` prints the name.'],
    ['The next exercises ask you to submit only a function definition.', 'The next exercises ask you to write only a function definition.'],
    ['Remove the temporary calls before submitting; the grader will make its own calls.', 'Remove the temporary calls before pressing **Check**; the tests make their own calls.'],
    ['An AI feedback tool may assess an explanation and ask follow-up questions. The tool is not meant to reward a particular phrase.', 'You can use this rubric to review an explanation yourself or discuss it with an AI assistant. This workshop app checks MCQs and Python programs; it does not assess written explanations.'],
    ["When the program works, step back from its individual lines and explain why its responsibilities are separated. The following exercise asks you to connect specific input, calculation, testing, and empty-case decisions to the program's behavior.", "When the program works, step back from its individual lines and explain why its responsibilities are separated. Connect specific input, calculation, testing, and empty-case decisions to the program's behavior."],
    ['reviews the part, asks you to complete a parcel-delivery program.', 'reviews the part and asks you to complete a parcel-delivery program.'],
  ];
  for (const [before, after] of replacements) text = text.replaceAll(before, after);
  text = text.replace(/\n## Put It All Together\n\s*(?=## )/g, '\n');
  text = text.replace(/\[recap\]/g, '[Recap]');
  if (id === 'part-1/1-overview') {
    text = text.replace(/1\. complete the background survey above;\n/, '').replace(/^[2-6]\. /gm, (prefix) => `${Number(prefix[0]) - 1}. `);
    text += '\n**Using this workshop app:** Enter all input lines before pressing **Run**. Use **Check** for automated feedback. Your drafts and progress are saved in this browser only.\n';
  }
  return text;
}
function write(filename, text, preserve = false) {
  if (preserve && fs.existsSync(filename)) return;
  fs.mkdirSync(path.dirname(filename), { recursive: true });
  fs.writeFileSync(filename, text);
}
function exportExercise(record, part, lessonId, sequence = null) {
  const data = record.data;
  const lang = data.languages?.en ?? {};
  let type = data.type;
  if (record.relative.startsWith('programming-pools/')) type = 'programming-exercise';
  if (data.tasks) {
    const retained = data.tasks.filter((task) => ['quiz', 'multiple-selection-quiz', 'programming-exercise'].includes(task.type));
    const omitted = data.tasks.filter((task) => !retained.includes(task));
    manifest.omitted.push(...omitted.map((task) => ({ id: task.uuid, type: task.type, lesson: lessonId })));
    if (!retained.length) return '';
    let intro = lang.handout?.trim() ?? '';
    const adaptedIntroductions = {
      'Identify what a dense expression computes, then rebuild it from named steps.': 'Identify what a dense expression computes. Consider which intermediate names would make it easier to read.',
      'Check an explanation against the code, then write an accurate replacement.': 'Check an explanation against the code and identify the accurate observations.',
      'Follow how a loop updates a Boolean flag, then repair a second version.': 'Repair a loop that updates a Boolean flag. Trace the flag after each value to check your repair.',
      'Trace a decomposed program and review two proposed refactorings.': 'Review two proposed refactorings of a decomposed program.',
    };
    intro = adaptedIntroductions[intro] ?? intro;
    return `\n${intro ? intro + '\n\n' : ''}${retained.sort((a, b) => a.order - b.order).map((task) => exportExercise({ ...record, data: task }, part, lessonId, data.uuid)).join('\n')}\n`;
  }
  if (!['quiz', 'multiple-selection-quiz', 'programming-exercise'].includes(type)) {
    manifest.omitted.push({ id: data.uuid, type: type ?? record.relative.split('/')[0], lesson: lessonId });
    return '';
  }
  const metadata = { id: data.uuid, type: type === 'programming-exercise' ? 'python' : 'mcq', title: lang.title ?? lang.name, prompt: lang.handout ?? '', part, points: data.points ?? 0 };
  const folder = path.join(destination, 'content/exercises', data.uuid);
  const origin = { id: data.uuid, lesson: lessonId, source: path.relative(source, record.filename), sequence };
  if (metadata.type === 'mcq') {
    metadata.multiple = type === 'multiple-selection-quiz';
    metadata.options = data.answers.map((answer) => ({ id: answer.uuid, text: answer.languages.en.text, correct: !!answer.correct, explanation: answer.languages.en.explanation ?? '' }));
  } else {
    const original = path.join(path.dirname(record.filename), ...(sequence ? [String(data.order)] : []));
    for (const [from, to] of [['starter/main.py', 'starter.py'], ['test/test.py', 'tests.py'], ['solution/main.py', 'solution.py']]) {
      const originalFile = path.join(original, from);
      if (fs.existsSync(originalFile)) write(path.join(folder, to), fs.readFileSync(originalFile, 'utf8'), true);
      else if (to === 'solution.py') manifest.solutionsMissingInSource.push({ id: data.uuid, title: metadata.title, source: path.relative(source, original) });
      else throw new Error(`Missing ${originalFile}`);
    }
    origin.files = path.relative(source, original);
  }
  if (!seen.has(data.uuid)) {
    write(path.join(folder, 'exercise.yml'), stringify(metadata, { lineWidth: 0 }));
    manifest.exercises.push(origin);
    seen.add(data.uuid);
  }
  return `:::exercise ${data.uuid}\n`;
}

for (let part = 1; part <= 3; part++) {
  const directory = path.join(materials, `part-${part}`);
  const filenames = fs.readdirSync(directory).filter((name) => name.endsWith('.mdx') && name !== 'index.mdx' && !name.includes('-games')).sort((a, b) => parseInt(a) - parseInt(b));
  const slugs = new Map(filenames.map((filename, index) => [filename.replace(/\.mdx$/, ''), filename.replace(/^\d+-/, `${index + 1}-`).replace(/\.mdx$/, '')]));
  for (const [index, filename] of filenames.entries()) {
    const original = path.join(directory, filename);
    let text = fs.readFileSync(original, 'utf8');
    const frontmatter = /^---\n([\s\S]*?)\n---\n/.exec(text);
    const header = parse(frontmatter[1]);
    const slug = slugs.get(filename.replace(/\.mdx$/, ''));
    const id = `part-${part}/${slug}`;
    const metadata = { id, part, order: index + 1, title: header.title.replace('Recap and Feedback', 'Recap') };
    text = text.slice(frontmatter[0].length);
    const imports = Object.fromEntries([...text.matchAll(/^import (\w+) from "([^"]+)";$/gm)].map((match) => [match[1], match[2]]));
    text = text.replace(/^import .*;\n/gm, '');
    text = text.replace(/\n## LEIA activity:[\s\S]*$/, '\n');
    text = text.replace(/\nStart with the lists-and-loops recap below\.\n/, '\n');
    text = text.replace(/\n## Feedback\n[\s\S]*?(?=\n## |$)/g, '\n');
    text = text.replace(/^.*\]\(\.\/(?:8-decisions-and-games|8-repetition-and-games|10-functions-and-games)\).*\n/gm, '');
    text = text.replace(/The Dice Combos example added one more question:\n\n> Can a larger rule use the result of a smaller function\?\n/, 'A larger function can use the result of a smaller function.');
    text = text.replace(/<Exercise\s+uuid="([^"]+)"[^>]*\/?>/g, (_, uuid) => {
      const record = registry.get(uuid);
      if (!record) throw new Error(`Unresolved exercise ${uuid} in ${id}`);
      return exportExercise(record, part, id);
    });
    let examples = 0;
    text = text.replace(/<Editor\s[\s\S]*?code=\{(`(?:\\.|[^`])*`)\}[\s\S]*?\/>/g, (_, literal) => {
      const code = vm.runInNewContext(literal, Object.create(null), { timeout: 100 });
      return `\n\`\`\`python runnable id=${id.replace('/', '-')}-example-${++examples}\n${code.trim()}\n\`\`\`\n`;
    });
    let steppers = 0;
    for (const match of [...text.matchAll(/<CodeStepper\s[^>]*content=\{(\w+)\}[^>]*\/>/g)]) {
      const modulePath = path.join(source, 'opencs-ui/src', imports[match[1]].replace(/^@\//, ''));
      const content = (await import(pathToFileURL(modulePath).href)).default;
      const outputs = content.stepEvents.filter((event) => event.type === 'output').map((event) => String(event.data));
      const narrative = outputs.length ? `Following the statements in execution order produces:\n\n\`\`\`text\n${outputs.join('\n')}\n\`\`\`` : 'Trace the statements in execution order, keeping track of each local name and the object it refers to.';
      const replacement = `\n\`\`\`python runnable id=${id.replace('/', '-')}-trace-${++steppers}\n${content.rawCode.trim()}\n\`\`\`\n\n${narrative}\n`;
      text = text.replace(match[0], replacement);
    }
    text = text.replace(/<ChapterDiagramGenerator[^>]*\/>/g, '');
    text = text.replace(/<LearningObjectives>/g, '## Learning Objectives').replace(/<\/LearningObjectives>/g, '');
    text = text.replace(/<InfoBox title="([^"]+)">/g, '**$1**').replace(/<\/InfoBox>/g, '');
    text = text.replace(/<br\s*\/>/g, '');
    text = text.replace(/\[([^\]]+)\]\(\.\/([^#)]+)(?:#([^)]*))?\)/g, (_, title, target, anchor) => `[${title}](#/part-${part}/${slugs.get(target) ?? target}${anchor ? `?anchor=${anchor}` : ''})`);
    text = text.replace(/recap and feedback/gi, 'recap').replace(/, and collects feedback on your experience\./g, '.').replace(/ and closes with feedback\./g, '.');
    text = text.replace('The button is in the top right corner of the editor below. ', '');
    text = adaptProse(text.replace(/\n{3,}/g, '\n\n'), id).replace(/\n{3,}/g, '\n\n').trim() + '\n';
    write(path.join(destination, 'content/lessons', `part-${part}`, `${slug}.md`), `---\n${stringify(metadata)}---\n\n${text}`);
    manifest.lessons.push({ id, source: path.relative(source, original), examples, steppers });
  }
}
write(path.join(destination, 'extraction-manifest.json'), JSON.stringify(manifest, null, 2) + '\n');
console.log(JSON.stringify({ lessons: manifest.lessons.length, exercises: manifest.exercises.length, solutionsMissingInSource: manifest.solutionsMissingInSource.length, inlineExamples: manifest.lessons.reduce((sum, lesson) => sum + lesson.examples, 0), steppers: manifest.lessons.reduce((sum, lesson) => sum + lesson.steppers, 0) }));
