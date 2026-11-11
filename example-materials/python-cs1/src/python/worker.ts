import type { PyodideAPI } from 'pyodide';
import supportSource from './workshop_support.py?raw';
import harnessSource from './harness.py?raw';
import type { WorkerRequest, WorkerResponse, RunResult } from './types';

let python: PyodideAPI | null = null;
const send = (message: WorkerResponse) => self.postMessage(message);

self.onmessage = async ({ data }: MessageEvent<WorkerRequest>) => {
  if (data.type === 'initialize') {
    try {
      // This URL always points at the app's self-hosted runtime, never a CDN.
      const { loadPyodide } = await import(/* @vite-ignore */ `${data.indexURL}pyodide.mjs`);
      python = await loadPyodide({ indexURL: data.indexURL });
      if (!python) throw new Error('Runtime initialization failed');
      python.FS.writeFile('/home/pyodide/workshop_support.py', supportSource);
      await python.runPythonAsync(harnessSource);
      send({ type: 'ready' });
    } catch (error) {
      send({ type: 'initialization-error', error: String(error) });
    }
    return;
  }
  if (!python) return;
  try {
    const execute = python.globals.get('workshop_execute');
    try {
      const result = JSON.parse(data.tests === undefined
        ? execute(data.code, data.input)
        : execute(data.code, data.input, data.tests)) as RunResult;
      send({ type: 'result', id: data.id, result });
    } finally {
      execute.destroy();
    }
  } catch (error) {
    send({ type: 'result', id: data.id, result: { stdout: '', stderr: '', error: String(error) } });
  }
};
