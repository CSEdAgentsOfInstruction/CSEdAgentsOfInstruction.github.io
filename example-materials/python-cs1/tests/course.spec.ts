import { test, expect, type Page, type Locator } from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';
import { parse } from 'yaml';

const content = path.resolve('content/exercises');
const manifest = JSON.parse(fs.readFileSync('extraction-manifest.json', 'utf8'));
const welcomeId = '55da8386-276f-429b-a161-4b77422a198a';
const singleId = '45696958-a59c-4479-8188-f7fb9ac70e67';
const welcomeStarter = fs.readFileSync(path.join(content, welcomeId, 'starter.py'), 'utf8');
const welcomeSolution = fs.readFileSync(path.join(content, welcomeId, 'solution.py'), 'utf8');
const metadata = (id: string) => parse(fs.readFileSync(path.join(content, id, 'exercise.yml'), 'utf8'));
const multiple = fs.readdirSync(content).map(metadata).find(exercise => exercise.multiple);

function lessonFor(id: string): string {
  return manifest.exercises.find((entry: { id: string }) => entry.id === id).lesson;
}

async function openExercise(page: Page, id: string): Promise<Locator> {
  await page.goto(`/#/${lessonFor(id)}`);
  const card = page.locator(`[data-exercise="${id}"]`);
  await expect(card).toBeVisible();
  return card;
}

async function setCode(page: Page, card: Locator, code: string) {
  const editor = card.getByTestId('code-input');
  await editor.click();
  await editor.press('ControlOrMeta+A');
  await page.keyboard.insertText(code);
}

async function run(card: Locator) {
  await card.getByRole('button', { name: /^Run / }).click();
  await expect(card.locator('.run-summary')).toBeVisible();
  await expect(card).not.toHaveAttribute('aria-busy', 'true');
}

test('all chapters navigate and an anchored lesson survives refresh', async ({ page }, testInfo) => {
  await page.goto('/');
  await expect(page.getByRole('navigation', { name: 'Course chapters' }).getByRole('link')).toHaveCount(26);
  await page.screenshot({ path: testInfo.outputPath('desktop-overview.png'), fullPage: true });
  await page.getByRole('link', { name: /Parameters and Return Values/ }).click();
  await expect(page.getByRole('heading', { level: 1 })).toHaveText('Parameters and Return Values');
  await page.goto('/#/part-1/4-values-variables-and-types?anchor=assignment-changes-state');
  await expect(page.locator('#assignment-changes-state')).toBeInViewport();
  await page.reload();
  await expect(page.getByRole('heading', { level: 1 })).toHaveText('Values, Variables, and Types');
  await expect(page.locator('#assignment-changes-state')).toBeInViewport();
});

test('single-choice answers require a selection, explain mistakes, and persist success', async ({ page }) => {
  const card = await openExercise(page, singleId);
  await card.getByRole('button', { name: 'Check answer', exact: true }).click();
  await expect(card.locator('.feedback')).toHaveText('Choose an answer first.');
  await card.getByRole('radio', { name: 'Output', exact: true }).check();
  await card.getByRole('button', { name: 'Check answer', exact: true }).click();
  await expect(card.locator('.feedback')).toContainText('Not quite.');
  await expect(card.locator('.answer-explanations')).toContainText('Python instruction');
  await card.getByRole('radio', { name: 'Code', exact: true }).check();
  await card.getByRole('button', { name: 'Check answer', exact: true }).click();
  await expect(card.locator('.feedback')).toContainText('Correct — well done.');
  await expect(card.locator('.completion-badge')).toBeVisible();
  await page.reload();
  await expect(card.getByRole('radio', { name: 'Code', exact: true })).toBeChecked();
  await expect(card.locator('.completion-badge')).toBeVisible();
  await card.getByRole('button', { name: 'Clear answer' }).click();
  await expect(card.locator('input:checked')).toHaveCount(0);
  await expect(card.locator('.completion-badge')).toBeHidden();
});

test('multiple selection accepts exactly the correct set, not a subset or superset', async ({ page }) => {
  const card = await openExercise(page, multiple.id);
  const correct = multiple.options.filter((option: { correct: boolean }) => option.correct);
  const wrong = multiple.options.find((option: { correct: boolean }) => !option.correct);
  expect(correct.length).toBeGreaterThan(1);
  await card.locator(`input[value="${correct[0].id}"]`).check();
  await card.getByRole('button', { name: 'Check answer', exact: true }).click();
  await expect(card.locator('.feedback')).toContainText('Not quite.');
  for (const option of correct) await card.locator(`input[value="${option.id}"]`).check();
  await card.getByRole('button', { name: 'Check answer', exact: true }).click();
  await expect(card.locator('.feedback')).toContainText('Correct — well done.');
  await card.locator(`input[value="${wrong.id}"]`).check();
  await card.getByRole('button', { name: 'Check answer', exact: true }).click();
  await expect(card.locator('.feedback')).toContainText('Not quite.');
  await expect(card.locator('.completion-badge')).toBeHidden();
});

test('real Python consumes Unicode and blank input lines and reports recoverable errors', async ({ page }) => {
  const card = await openExercise(page, welcomeId);
  await setCode(page, card, 'values = [input("First: "), input("Second: "), input("Third: ")]\nprint(repr(values))');
  await card.getByLabel('Program input', { exact: true }).fill('Åda\n\n雪');
  await run(card);
  await expect(card.getByLabel('Program output', { exact: true })).toHaveText("First: Second: Third: ['Åda', '', '雪']\n");

  await setCode(page, card, 'print(input())');
  await card.getByLabel('Program input', { exact: true }).fill('');
  await run(card);
  await expect(card.getByLabel('Python errors', { exact: true })).toContainText('EOFError');

  await setCode(page, card, 'print(');
  await run(card);
  await expect(card.getByLabel('Python errors', { exact: true })).toContainText('SyntaxError');

  await setCode(page, card, 'print("recovered")');
  await run(card);
  await expect(card.getByLabel('Program output', { exact: true })).toHaveText('recovered\n');
  await expect(card.getByLabel('Python errors', { exact: true })).toHaveCount(0);
});

test('checks use actual Python tests and reveal/reset preserve the exercise workflow', async ({ page }, testInfo) => {
  const card = await openExercise(page, welcomeId);
  await expect(card.locator('.reference-code')).toBeHidden();
  await card.getByText('Reveal reference solution', { exact: true }).click();
  await expect(card.locator('.reference-code')).toHaveText(welcomeSolution);

  await setCode(page, card, 'print("Wrong answer")');
  await card.getByRole('button', { name: 'Check Welcome card', exact: true }).click();
  await expect(card.locator('.run-summary')).toHaveText('Some checks need attention.');
  await expect(card.locator('.test-fail')).not.toHaveCount(0);
  await setCode(page, card, welcomeSolution);
  await card.getByRole('button', { name: 'Check Welcome card', exact: true }).click();
  await expect(card.locator('.run-summary')).toHaveText('All checks passed.');
  await expect(card.locator('.completion-badge')).toBeVisible();
  await card.screenshot({ path: testInfo.outputPath('desktop-python-exercise.png') });
  await page.reload();
  await expect(card.locator('.completion-badge')).toBeVisible();
  await card.getByLabel('Program input', { exact: true }).fill('saved input');
  await card.getByRole('button', { name: 'Reset Welcome card to starter', exact: true }).click();
  await expect(card.getByLabel('Program input', { exact: true })).toHaveValue('');
  await expect(card.locator('.completion-badge')).toBeHidden();
  const state = await page.evaluate(id => JSON.parse(localStorage.getItem(`python-workshop:v1:${id}`)!), welcomeId);
  expect(state.code).toBe(welcomeStarter);
  expect(state.completed).toBe(false);
});

test('Stop and execution timeout terminate loops and allow a fresh successful run', async ({ page }) => {
  const card = await openExercise(page, welcomeId);
  await setCode(page, card, 'while True:\n    pass');
  await card.getByRole('button', { name: 'Run Welcome card', exact: true }).click();
  await expect(card.locator('.runtime-status')).toHaveText('Running…');
  await card.getByRole('button', { name: 'Stop', exact: true }).click();
  await expect(card.locator('.run-summary')).toContainText('Execution stopped.');
  await expect(card.getByTestId('code-input')).toContainText('while True:');
  await setCode(page, card, 'print("after stop")');
  await run(card);
  await expect(card.getByLabel('Program output', { exact: true })).toHaveText('after stop\n');

  await setCode(page, card, 'while True:\n    pass');
  await run(card);
  await expect(card.locator('.run-summary')).toContainText('Execution stopped after 10 seconds.');
  await setCode(page, card, 'print("after timeout")');
  await run(card);
  await expect(card.getByLabel('Program output', { exact: true })).toHaveText('after timeout\n');
});

test('drafts survive reload and changed source starters require an explicit choice', async ({ page }) => {
  const card = await openExercise(page, welcomeId);
  await setCode(page, card, 'print("my workshop draft")');
  await card.getByLabel('Program input', { exact: true }).fill('Åda\nsecond line');
  await page.reload();
  await expect(card.getByTestId('code-input')).toContainText('my workshop draft');
  await expect(card.getByLabel('Program input', { exact: true })).toHaveValue('Åda\nsecond line');

  await page.evaluate(id => {
    const key = `python-workshop:v1:${id}`;
    const saved = JSON.parse(localStorage.getItem(key)!);
    localStorage.setItem(key, JSON.stringify({ ...saved, starter: '# earlier source starter\n' }));
  }, welcomeId);
  await page.reload();
  await expect(card.locator('.starter-notice')).toBeVisible();
  await card.getByRole('button', { name: 'Keep my draft', exact: true }).click();
  await expect(card.locator('.starter-notice')).toBeHidden();
  await page.reload();
  await expect(card.getByTestId('code-input')).toContainText('my workshop draft');
  await expect(card.locator('.starter-notice')).toBeHidden();

  await page.evaluate(id => {
    const key = `python-workshop:v1:${id}`;
    const saved = JSON.parse(localStorage.getItem(key)!);
    localStorage.setItem(key, JSON.stringify({ ...saved, starter: '# another earlier source starter\n' }));
  }, welcomeId);
  await page.reload();
  await card.getByRole('button', { name: 'Load updated starter', exact: true }).click();
  await expect(card.locator('.starter-notice')).toBeHidden();
  const saved = await page.evaluate(id => JSON.parse(localStorage.getItem(`python-workshop:v1:${id}`)!), welcomeId);
  expect(saved.code).toBe(welcomeStarter);
  expect(saved.starter).toBe(welcomeStarter);
});

test('a failed runtime download leaves code intact and can be retried', async ({ page }) => {
  const card = await openExercise(page, welcomeId);
  await setCode(page, card, 'print("retry succeeded")');
  // Fail the entry module, which rejects immediately. A stalled WASM load is
  // separately bounded by the client's 60-second initialization timeout.
  await page.context().route('**/pyodide/pyodide.mjs', route => route.abort('failed'));
  await run(card);
  await expect(card.locator('.run-summary')).toContainText(/could not load|stopped unexpectedly|failed|fetch/i);
  await expect(card.getByTestId('code-input')).toContainText('retry succeeded');
  await page.context().unroute('**/pyodide/pyodide.mjs');
  await run(card);
  await expect(card.getByLabel('Program output', { exact: true })).toHaveText('retry succeeded\n');
});

test('a narrow screen keeps the editor and controls within the viewport', async ({ page }, testInfo) => {
  await page.setViewportSize({ width: 375, height: 812 });
  const card = await openExercise(page, welcomeId);
  await expect(card.getByRole('button', { name: 'Run Welcome card', exact: true })).toBeVisible();
  const geometry = await page.evaluate(() => ({ width: document.documentElement.clientWidth, scrollWidth: document.documentElement.scrollWidth }));
  expect(geometry.scrollWidth).toBeLessThanOrEqual(geometry.width);
  await card.scrollIntoViewIfNeeded();
  await page.screenshot({ path: testInfo.outputPath('mobile-python-exercise.png') });
});
