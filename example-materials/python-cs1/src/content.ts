import { parseExerciseYaml, parseFrontmatter } from './content-format';
import type { Exercise, Lesson } from './types';

const lessonSources = import.meta.glob('../content/lessons/**/*.md', { query: '?raw', import: 'default', eager: true }) as Record<string, string>;
const exerciseSources = import.meta.glob('../content/exercises/*/exercise.yml', { query: '?raw', import: 'default', eager: true }) as Record<string, string>;
const pythonSources = import.meta.glob('../content/exercises/*/*.py', { query: '?raw', import: 'default', eager: true }) as Record<string, string>;

export const lessons: Lesson[] = Object.entries(lessonSources).map(([path, source]) => {
  const { metadata, body } = parseFrontmatter(source);
  for (const field of ['id', 'title']) {
    if (typeof metadata[field] !== 'string') throw new Error(`${path}: missing ${field}`);
  }
  if (!Number.isInteger(metadata.part) || !Number.isInteger(metadata.order)) throw new Error(`${path}: part and order must be integers`);
  return { ...metadata, body } as unknown as Lesson;
}).sort((a, b) => a.part - b.part || a.order - b.order);

export const exercises = new Map<string, Exercise>();
for (const [path, source] of Object.entries(exerciseSources)) {
  const metadata = parseExerciseYaml(source);
  if (typeof metadata.id !== 'string' || !['mcq', 'python'].includes(String(metadata.type))) throw new Error(`${path}: invalid exercise ID or type`);
  if (exercises.has(metadata.id)) throw new Error(`Duplicate exercise ID: ${metadata.id}`);
  const exercise = metadata as unknown as Exercise;
  if (exercise.type === 'python') {
    const directory = path.slice(0, path.lastIndexOf('/'));
    exercise.starter = pythonSources[`${directory}/starter.py`];
    exercise.tests = pythonSources[`${directory}/tests.py`];
    exercise.solution = pythonSources[`${directory}/solution.py`];
    if (exercise.starter === undefined || exercise.tests === undefined) throw new Error(`${path}: starter.py or tests.py missing`);
  }
  exercises.set(exercise.id, exercise);
}

export const partTitles: Record<number, string> = {
  1: 'Making Decisions',
  2: 'Repeating and Remembering',
  3: 'Building from Pieces',
};
