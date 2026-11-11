import { parse } from 'yaml';

/** Kept separate from Vite so authoring tools can use the same format. */
export function parseFrontmatter(source: string): { metadata: Record<string, unknown>; body: string } {
  const match = source.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/);
  if (!match) throw new Error('Lesson is missing YAML frontmatter.');
  const metadata = parse(match[1]);
  if (!metadata || typeof metadata !== 'object' || Array.isArray(metadata)) {
    throw new Error('Lesson frontmatter must be a YAML mapping.');
  }
  return { metadata, body: source.slice(match[0].length) };
}

export function parseExerciseYaml(source: string): Record<string, unknown> {
  const exercise = parse(source);
  if (!exercise || typeof exercise !== 'object' || Array.isArray(exercise)) {
    throw new Error('Exercise metadata must be a YAML mapping.');
  }
  return exercise;
}
