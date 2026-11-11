import { EditorView, basicSetup } from 'codemirror';
import { python } from '@codemirror/lang-python';
import { marked } from 'marked';
import DOMPurify from 'dompurify';
import { exercises, lessons, partTitles } from './content';
import { PythonRunner } from './python/client';
import type { Draft, Exercise, Lesson } from './types';
import './style.css';

const app = document.querySelector<HTMLDivElement>('#app')!;
const storagePrefix = 'python-workshop:v1:';
const memoryStorage = new Map<string, string>();
let storageAvailable = true;
let disposeLesson = () => {};
let currentLesson: Lesson | undefined;

function element<K extends keyof HTMLElementTagNameMap>(tag: K, className = '', text = ''): HTMLElementTagNameMap[K] {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text) node.textContent = text;
  return node;
}

function button(text: string, className: string, action: () => void) {
  const node = element('button', className, text);
  node.type = 'button';
  node.addEventListener('click', action);
  return node;
}

function readSaved<T>(id: string): T | undefined {
  try {
    const raw = memoryStorage.get(id) ?? localStorage.getItem(storagePrefix + id);
    return raw ? JSON.parse(raw) as T : undefined;
  } catch { return undefined; }
}

function save(id: string, value: unknown) {
  const raw = JSON.stringify(value);
  memoryStorage.set(id, raw);
  try { localStorage.setItem(storagePrefix + id, raw); }
  catch { storageAvailable = false; }
  updateProgress();
}

function updateProgress() {
  const completed = [...exercises.keys()].filter(id => readSaved<{ completed?: boolean }>(id)?.completed).length;
  document.querySelectorAll<HTMLElement>('[data-progress]').forEach(node => {
    node.textContent = `${completed} of ${exercises.size} exercises completed`;
  });
  document.querySelectorAll<HTMLElement>('[data-storage-note]').forEach(node => {
    node.textContent = storageAvailable ? 'Progress stays in this browser.' : 'Browser storage is unavailable. Keep this tab open to retain your work.';
  });
}

function lessonUrl(lesson: Lesson | string, anchor?: string) {
  return `#/${typeof lesson === 'string' ? lesson : lesson.id}${anchor ? `?anchor=${encodeURIComponent(anchor)}` : ''}`;
}

function slugify(text: string) {
  return text.toLowerCase().trim().replace(/[^\p{L}\p{N}\s-]/gu, '').replace(/[\s-]+/g, '-');
}

function contentRevision(value: string) {
  // This detects edited teaching material; it is not a security checksum.
  let hash = 2166136261;
  for (let i = 0; i < value.length; i++) hash = Math.imul(hash ^ value.charCodeAt(i), 16777619);
  return (hash >>> 0).toString(16);
}

function markdown(source: string, lesson = currentLesson): HTMLElement {
  const container = element('div', 'markdown');
  container.innerHTML = DOMPurify.sanitize(marked.parse(source, { async: false }) as string);
  for (const link of container.querySelectorAll<HTMLAnchorElement>('a[href]')) {
    const href = link.getAttribute('href')!;
    if (/^https?:\/\//.test(href)) {
      link.target = '_blank';
      link.rel = 'noopener noreferrer';
      continue;
    }
    if (!lesson || href.startsWith('#/') || /^(mailto:|tel:)/.test(href)) continue;
    if (href.startsWith('#')) { link.href = lessonUrl(lesson, href.slice(1)); continue; }
    const [rawPath, anchor] = href.split('#');
    const path = rawPath.replace(/\.mdx?$/, '').replace(/\/$/, '');
    const base = new URL(`${lesson.id}/../`, 'https://course.invalid/');
    const resolved = new URL(path, base).pathname.slice(1).replace(/^.*introduction-to-programming\//, '');
    const target = lessons.find(item => item.id === resolved);
    if (target) link.href = lessonUrl(target, anchor);
  }
  return container;
}

function exerciseHeading(exercise: Exercise, kind: string) {
  const heading = element('div', 'exercise-heading');
  const label = element('span', 'exercise-label', kind);
  const complete = element('span', 'completion-badge', 'Complete');
  complete.hidden = !readSaved<{ completed?: boolean }>(exercise.id)?.completed;
  complete.dataset.completion = exercise.id;
  heading.append(label, complete);
  return heading;
}

function setCompletion(id: string, completed: boolean) {
  document.querySelectorAll<HTMLElement>('[data-completion]').forEach(node => {
    if (node.dataset.completion === id) node.hidden = !completed;
  });
}

function renderMcq(exercise: Exercise) {
  const card = element('section', 'exercise mcq-exercise');
  card.dataset.exercise = exercise.id;
  card.dataset.testid = 'mcq-exercise';
  const titleId = `exercise-${exercise.id}`;
  card.setAttribute('aria-labelledby', titleId);
  card.append(exerciseHeading(exercise, exercise.multiple ? 'MULTIPLE SELECTION' : 'MULTIPLE CHOICE'));
  const title = element('h3', 'exercise-title', exercise.title);
  title.id = titleId;
  card.append(title, markdown(exercise.prompt));
  const fieldset = element('fieldset', 'choices');
  const legend = element('legend', 'choice-instruction', exercise.multiple ? 'Select all correct answers.' : 'Select one answer.');
  fieldset.append(legend);
  const fingerprint = JSON.stringify([exercise.prompt, exercise.options]);
  const saved = readSaved<{ selected: string[]; fingerprint: string; completed: boolean }>(exercise.id);
  let completed = saved?.fingerprint === fingerprint && Boolean(saved.completed);
  setTimeout(() => setCompletion(exercise.id, completed), 0);
  const feedback = element('div', 'feedback');
  feedback.setAttribute('aria-live', 'polite');
  const inputs: HTMLInputElement[] = [];
  const selected = () => inputs.filter(input => input.checked).map(input => input.value);
  const persist = () => save(exercise.id, { selected: selected(), fingerprint, completed });
  for (const choice of exercise.options ?? []) {
    const label = element('label', 'choice');
    const input = element('input');
    input.type = exercise.multiple ? 'checkbox' : 'radio';
    input.name = exercise.id;
    input.value = choice.id;
    input.checked = Boolean(saved?.selected?.includes(choice.id));
    input.addEventListener('change', () => {
      completed = false;
      feedback.replaceChildren();
      feedback.className = 'feedback';
      setCompletion(exercise.id, false);
      persist();
    });
    inputs.push(input);
    label.append(input, markdown(choice.text));
    fieldset.append(label);
  }
  const controls = element('div', 'exercise-actions');
  const check = button('Check answer', 'button primary', () => {
    const chosen = new Set(selected());
    if (!chosen.size) {
      feedback.className = 'feedback warning';
      feedback.textContent = 'Choose an answer first.';
      return;
    }
    completed = (exercise.options ?? []).every(choice => chosen.has(choice.id) === choice.correct);
    feedback.className = `feedback ${completed ? 'success' : 'warning'}`;
    feedback.replaceChildren(element('p', 'feedback-title', completed ? 'Correct — well done.' : 'Not quite. Review the explanations and try again.'));
    const explanations = element('div', 'answer-explanations');
    for (const choice of exercise.options ?? []) {
      if (!choice.explanation) continue;
      const explanation = element('div', 'answer-explanation');
      explanation.append(element('span', 'answer-tag', choice.correct ? 'Correct choice' : 'Other choice'), markdown(choice.text), markdown(choice.explanation));
      explanations.append(explanation);
    }
    feedback.append(explanations);
    setCompletion(exercise.id, completed);
    persist();
  });
  const retry = button('Clear answer', 'button quiet', () => {
    inputs.forEach(input => { input.checked = false; });
    completed = false;
    feedback.replaceChildren();
    feedback.className = 'feedback';
    setCompletion(exercise.id, false);
    persist();
  });
  controls.append(check, retry);
  card.append(fieldset, controls, feedback);
  if (saved && saved.fingerprint !== fingerprint) persist();
  return card;
}

interface PythonCardOptions {
  id: string;
  title: string;
  starter: string;
  prompt?: string;
  tests?: string;
  solution?: string;
  exercise?: Exercise;
}

interface LessonRuntime {
  runner: PythonRunner;
  buttons: Set<HTMLButtonElement>;
  activeStatus?: HTMLElement;
  busy: boolean;
  cleanups: (() => void)[];
}

function renderPython(options: PythonCardOptions, runtime: LessonRuntime) {
  const { id, title, starter, tests, solution, exercise } = options;
  const card = element('section', `exercise python-exercise${exercise ? '' : ' runnable-example'}`);
  card.dataset.exercise = id;
  card.dataset.testid = exercise ? 'python-exercise' : 'runnable-example';
  const heading = element('h3', 'exercise-title', title);
  heading.id = `exercise-${id}`;
  card.setAttribute('aria-labelledby', heading.id);
  if (exercise) card.append(exerciseHeading(exercise, 'PYTHON EXERCISE'));
  else card.append(element('div', 'exercise-label', 'TRY IT · PYTHON'));
  if (exercise) card.append(heading);
  else { heading.classList.add('sr-only'); card.append(heading); }
  if (options.prompt) card.append(markdown(options.prompt));

  const saved = readSaved<Draft>(id);
  const draft = saved && typeof saved.code === 'string' && typeof saved.starter === 'string' ? saved : undefined;
  const revision = contentRevision(JSON.stringify([starter, tests, options.prompt]));
  let acceptedStarter = draft?.starter ?? starter;
  let completed = Boolean(draft?.completed && draft.starter === starter && draft.revision === revision);
  const changed = element('div', 'starter-notice');
  changed.hidden = !draft || draft.starter === starter;
  changed.append(element('p', '', 'The source starter has changed. Keep your saved work or load the updated starter.'));
  const editorHeader = element('div', 'editor-header');
  editorHeader.append(element('span', 'filename', 'main.py'), element('span', 'editor-language', 'Python'));
  const editorHost = element('div', 'code-editor');
  const inputId = `input-${id}`;
  const inputLabel = element('label', 'input-label', 'Program input');
  inputLabel.htmlFor = inputId;
  const input = element('textarea', 'program-input');
  input.id = inputId;
  input.rows = 2;
  input.spellcheck = false;
  input.placeholder = 'Enter one answer per line before running';
  input.value = typeof draft?.input === 'string' ? draft.input : '';
  const inputHelp = element('p', 'input-help', 'Each input() reads the next line. Leave this empty if your program needs no input.');
  inputHelp.id = `${inputId}-help`;
  input.setAttribute('aria-describedby', inputHelp.id);
  const persist = () => save(id, { starter: acceptedStarter, code: editor.state.doc.toString(), input: input.value, completed, revision });
  const editor = new EditorView({
    doc: draft?.code ?? starter,
    extensions: [basicSetup, python(), EditorView.lineWrapping,
      EditorView.contentAttributes.of({ 'aria-label': `Python code for ${title}`, 'data-testid': 'code-input', autocorrect: 'off', autocapitalize: 'off', spellcheck: 'false' }),
      EditorView.updateListener.of(update => {
        if (update.docChanged) {
          completed = false;
          setCompletion(id, false);
          persist();
        }
      }),
      EditorView.theme({ '&': { fontSize: '14px' }, '.cm-content': { minHeight: '110px', padding: '14px 0', fontFamily: '"SFMono-Regular", Consolas, "Liberation Mono", monospace' }, '.cm-gutters': { backgroundColor: '#f3f5f4', color: '#82918c', border: 'none' }, '.cm-activeLine, .cm-activeLineGutter': { backgroundColor: '#e7f2ee66' }, '&.cm-focused': { outline: '2px solid #277369', outlineOffset: '-2px' }, '.cm-scroller': { maxHeight: '470px', overflow: 'auto' } }),
    ],
    parent: editorHost,
  });
  runtime.cleanups.push(() => editor.destroy());
  input.addEventListener('input', persist);
  const acceptStarter = (load: boolean) => {
    acceptedStarter = starter;
    if (load) editor.dispatch({ changes: { from: 0, to: editor.state.doc.length, insert: starter } });
    changed.hidden = true;
    completed = false;
    setCompletion(id, false);
    persist();
  };
  const noticeActions = element('div', 'exercise-actions');
  noticeActions.append(button('Keep my draft', 'button secondary', () => acceptStarter(false)), button('Load updated starter', 'button quiet', () => acceptStarter(true)));
  changed.append(noticeActions);
  const controls = element('div', 'exercise-actions run-actions');
  const status = element('span', 'runtime-status');
  status.setAttribute('aria-live', 'polite');
  const output = element('div', 'execution-output');
  output.setAttribute('aria-live', 'polite');
  output.setAttribute('aria-atomic', 'false');
  const stop = button('Stop', 'button stop', () => runtime.runner.stop());
  stop.hidden = true;

  const run = async (check: boolean) => {
    if (runtime.busy) return;
    runtime.busy = true;
    runtime.activeStatus = status;
    runtime.buttons.forEach(control => { control.disabled = true; });
    stop.hidden = false;
    input.disabled = true;
    const code = editor.state.doc.toString();
    output.replaceChildren();
    card.setAttribute('aria-busy', 'true');
    try {
      const result = await runtime.runner.run(code, input.value, check ? tests : undefined);
      if (!card.isConnected) return;
      const codeChanged = editor.state.doc.toString() !== code;
      if (check) {
        completed = result.passed === true && !codeChanged;
        setCompletion(id, completed);
        persist();
      }
      const headingText = result.error ? result.error : check ? (result.passed ? 'All checks passed.' : 'Some checks need attention.') : 'Program finished.';
      const summary = element('p', `run-summary ${result.error || (check && !result.passed) ? 'result-warning' : 'result-success'}`, headingText);
      output.append(summary);
      if (codeChanged) output.append(element('p', 'input-help', 'The code changed during execution. Run or check it again for an up-to-date result.'));
      if (result.stdout) {
        const label = element('h4', 'output-label', 'Output');
        const pre = element('pre', 'console-output', result.stdout);
        pre.setAttribute('aria-label', 'Program output');
        output.append(label, pre);
      }
      if (result.stderr) {
        const label = element('h4', 'output-label', 'Python messages');
        const pre = element('pre', 'console-output error-output', result.stderr);
        pre.setAttribute('aria-label', 'Python errors');
        output.append(label, pre);
      }
      if (!result.stdout && !result.stderr && !check && !result.error) output.append(element('p', 'input-help', 'The program produced no output.'));
      if (result.tests?.length) {
        const list = element('ul', 'test-results');
        for (const test of result.tests) {
          const item = element('li', test.passed ? 'test-pass' : 'test-fail');
          const details = element('details');
          details.open = !test.passed;
          const summary = element('summary', '', `${test.passed ? '✓' : '×'} ${test.name}`);
          details.append(summary);
          if (test.message) details.append(element('pre', 'test-message', test.message));
          item.append(details);
          list.append(item);
        }
        output.append(list);
      }
    } catch (error) {
      output.append(element('p', 'run-summary result-warning', error instanceof Error ? error.message : String(error)));
    } finally {
      runtime.busy = false;
      runtime.activeStatus = undefined;
      runtime.buttons.forEach(control => { control.disabled = false; });
      stop.hidden = true;
      input.disabled = false;
      status.textContent = '';
      card.removeAttribute('aria-busy');
    }
  };
  const runButton = button('Run', 'button primary', () => { void run(false); });
  runButton.setAttribute('aria-label', `Run ${title}`);
  runtime.buttons.add(runButton);
  controls.append(runButton);
  if (tests !== undefined) {
    const check = button('Check', 'button secondary', () => { void run(true); });
    check.setAttribute('aria-label', `Check ${title}`);
    runtime.buttons.add(check);
    controls.append(check);
  }
  const reset = button('Reset', 'button quiet', () => {
    acceptStarter(true);
    input.value = '';
    persist();
    output.replaceChildren();
  });
  reset.setAttribute('aria-label', `Reset ${title} to starter`);
  runtime.buttons.add(reset);
  controls.append(stop, reset, status);
  const inputGroup = element('div', 'input-group');
  inputGroup.append(inputLabel, input, inputHelp);
  card.append(changed, editorHeader, editorHost, inputGroup, controls, output);
  if (solution !== undefined) {
    const reference = element('details', 'reference-solution');
    reference.append(element('summary', '', 'Reveal reference solution'), element('p', 'input-help', 'One possible solution. Your program may take a different approach.'), element('pre', 'reference-code', solution));
    card.append(reference);
  }
  if (exercise && draft && !completed && draft.completed) {
    persist();
    setTimeout(() => setCompletion(id, false), 0);
  }
  return card;
}

function renderLessonBody(lesson: Lesson, runtime: LessonRuntime) {
  const body = element('div', 'lesson-body');
  const lines = lesson.body.split('\n');
  let buffer: string[] = [];
  let example = 0;
  const flush = () => {
    if (buffer.some(line => line.trim())) body.append(markdown(buffer.join('\n'), lesson));
    buffer = [];
  };
  for (let i = 0; i < lines.length; i++) {
    const exerciseMatch = lines[i].match(/^:::exercise\s+(?:\{?id=["']?)?([\w-]+)["']?\}?\s*$/);
    if (exerciseMatch) {
      flush();
      const exercise = exercises.get(exerciseMatch[1]);
      if (exercise) body.append(exercise.type === 'mcq' ? renderMcq(exercise) : renderPython({ id: exercise.id, title: exercise.title, starter: exercise.starter!, tests: exercise.tests, solution: exercise.solution, prompt: exercise.prompt, exercise }, runtime));
      else body.append(element('div', 'content-error', `Exercise ${exerciseMatch[1]} could not be found. Check its lesson reference and metadata.`));
      if (lines[i + 1]?.trim() === ':::') i++;
      continue;
    }
    const fence = lines[i].match(/^\s*(`{3,}|~{3,})(.*)$/);
    if (fence) {
      const start = i;
      const info = fence[2].trim();
      const closing = new RegExp(`^\\s*${fence[1][0]}{${fence[1].length},}\\s*$`);
      const code: string[] = [];
      for (i++; i < lines.length && !closing.test(lines[i]); i++) code.push(lines[i]);
      if (/^python\b/.test(info) && /\brunnable\b/.test(info)) {
        flush();
        example++;
        const declaredId = info.match(/\bid=["']?([^\s"']+)/)?.[1];
        body.append(renderPython({ id: `example:${lesson.id}:${declaredId ?? example}`, title: `Example ${example}`, starter: code.join('\n') + '\n' }, runtime));
      } else buffer.push(...lines.slice(start, Math.min(i + 1, lines.length)));
      continue;
    }
    buffer.push(lines[i]);
  }
  flush();
  const headingCounts = new Map<string, number>();
  for (const heading of body.querySelectorAll<HTMLElement>('.markdown h1, .markdown h2, .markdown h3, .markdown h4')) {
    const slug = slugify(heading.textContent ?? 'section');
    const count = headingCounts.get(slug) ?? 0;
    headingCounts.set(slug, count + 1);
    heading.id = count ? `${slug}-${count}` : slug;
  }
  return body;
}

function renderShell() {
  app.replaceChildren();
  const header = element('header', 'site-header');
  const brand = element('a', 'brand');
  brand.href = lessons[0] ? lessonUrl(lessons[0]) : '#/';
  brand.setAttribute('aria-label', 'Introduction to Programming home');
  brand.append(element('span', 'brand-mark', 'py'), element('span', 'brand-name', 'Programming, piece by piece'));
  const edition = element('span', 'edition-label', 'AGENTS OF INSTRUCTION · WORKSHOP EDITION');
  header.append(brand, edition);
  const layout = element('div', 'course-layout');
  const aside = element('aside', 'sidebar');
  const toc = element('details', 'course-navigation');
  const wideLayout = window.matchMedia('(min-width: 761px)');
  toc.open = wideLayout.matches;
  wideLayout.addEventListener('change', event => { toc.open = event.matches; });
  const tocSummary = element('summary', 'toc-summary', 'Course contents');
  toc.append(tocSummary);
  const nav = element('nav');
  nav.setAttribute('aria-label', 'Course chapters');
  const intro = element('div', 'sidebar-intro');
  intro.append(element('p', 'eyebrow', 'INTRODUCTION TO PROGRAMMING'), element('p', 'sidebar-description', 'Read, experiment, and make it your own.'));
  nav.append(intro);
  for (const part of [...new Set(lessons.map(lesson => lesson.part))]) {
    const group = element('div', 'part-group');
    const heading = element('h2', 'part-heading');
    heading.append(element('span', 'part-number', String(part).padStart(2, '0')), element('span', '', partTitles[part] ?? `Part ${part}`));
    group.append(heading);
    const list = element('ol', 'chapter-list');
    for (const lesson of lessons.filter(item => item.part === part)) {
      const item = element('li');
      const link = element('a', 'chapter-link');
      link.href = lessonUrl(lesson);
      link.dataset.lesson = lesson.id;
      link.append(element('span', 'chapter-number', String(lesson.order).padStart(2, '0')), element('span', '', lesson.title));
      item.append(link);
      list.append(item);
    }
    group.append(list);
    nav.append(group);
  }
  toc.append(nav);
  const progress = element('div', 'local-progress');
  const progressText = element('p', 'progress-text');
  progressText.dataset.progress = '';
  const storageNote = element('p', 'storage-note');
  storageNote.dataset.storageNote = '';
  progress.append(progressText, storageNote);
  aside.append(toc, progress);
  const main = element('main', 'main-content');
  main.id = 'main-content';
  main.tabIndex = -1;
  layout.append(aside, main);
  app.append(header, layout);
  document.querySelector('.skip-link')?.addEventListener('click', event => {
    event.preventDefault();
    main.focus();
    main.scrollIntoView();
  });
  updateProgress();
}

function route() {
  const fragment = location.hash.replace(/^#\/?/, '');
  const [id, query = ''] = fragment.split('?');
  const lesson = lessons.find(item => item.id === decodeURIComponent(id)) ?? lessons[0];
  const anchor = new URLSearchParams(query).get('anchor');
  if (!lesson) {
    document.querySelector('main')!.replaceChildren(element('h1', '', 'No lessons found'), element('p', '', 'Add lessons to content/lessons to get started.'));
    return;
  }
  if (!id) history.replaceState(null, '', lessonUrl(lesson));
  const sameLesson = currentLesson?.id === lesson.id;
  if (!sameLesson) {
    disposeLesson();
    currentLesson = lesson;
    const runtime: LessonRuntime = { runner: undefined as unknown as PythonRunner, buttons: new Set(), busy: false, cleanups: [] };
    runtime.runner = new PythonRunner(status => {
      if (runtime.activeStatus) runtime.activeStatus.textContent = status === 'loading' ? 'Loading Python…' : status === 'running' ? 'Running…' : '';
    });
    disposeLesson = () => { runtime.runner.dispose(); runtime.cleanups.forEach(cleanup => cleanup()); };
    const main = document.querySelector<HTMLElement>('main')!;
    const article = element('article', 'lesson');
    const header = element('header', 'lesson-header');
    header.append(element('p', 'eyebrow', `PART ${String(lesson.part).padStart(2, '0')} · CHAPTER ${String(lesson.order).padStart(2, '0')}`), element('h1', '', lesson.title));
    const subtitle = element('p', 'lesson-context', `${partTitles[lesson.part] ?? `Part ${lesson.part}`} / Introduction to Programming`);
    header.append(subtitle);
    article.append(header, renderLessonBody(lesson, runtime));
    const index = lessons.indexOf(lesson);
    const pagination = element('nav', 'lesson-pagination');
    pagination.setAttribute('aria-label', 'Previous and next chapters');
    for (const [offset, label] of [[-1, 'Previous chapter'], [1, 'Next chapter']] as const) {
      const target = lessons[index + offset];
      if (target) {
        const link = element('a', `pagination-link ${offset === 1 ? 'next' : 'previous'}`);
        link.href = lessonUrl(target);
        link.append(element('span', 'pagination-label', `${offset === -1 ? '← ' : ''}${label}${offset === 1 ? ' →' : ''}`), element('span', '', target.title));
        pagination.append(link);
      } else pagination.append(element('span'));
    }
    const footer = element('footer', 'lesson-footer', 'Workshop materials · Python runs in your browser · Tests and solutions are included for adaptation.');
    article.append(pagination, footer);
    main.replaceChildren(article);
    document.title = `${lesson.title} · Introduction to Programming`;
    document.querySelectorAll<HTMLAnchorElement>('[data-lesson]').forEach(link => {
      if (link.dataset.lesson === lesson.id) link.setAttribute('aria-current', 'page');
      else link.removeAttribute('aria-current');
    });
    updateProgress();
  }
  requestAnimationFrame(() => {
    if (anchor) document.getElementById(anchor)?.scrollIntoView({ block: 'start' });
    else if (!sameLesson) window.scrollTo({ top: 0 });
  });
}

renderShell();
route();
window.addEventListener('hashchange', route);
window.addEventListener('beforeunload', () => disposeLesson());
