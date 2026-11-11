import type { RunResult, WorkerResponse } from './types';

export type { RunResult, TestResult } from './types';

/** Owns one worker at a time. Termination works even while Python is in a loop. */
export class PythonRunner {
  private worker: Worker | null = null;
  private ready: Promise<void> | null = null;
  private rejectReady: ((error: Error) => void) | null = null;
  private timer: ReturnType<typeof setTimeout> | null = null;
  private pending: { id: number; resolve: (result: RunResult) => void } | null = null;
  private nextId = 0;

  constructor(private onStatus: (status: 'loading' | 'running' | 'idle') => void = () => {}) {}

  private initialize(): Promise<void> {
    if (this.ready) return this.ready;
    this.onStatus('loading');
    const worker = new Worker(new URL('./worker.ts', import.meta.url), { type: 'module' });
    this.worker = worker;
    this.ready = new Promise<void>((resolve, reject) => {
      this.rejectReady = reject;
      this.timer = setTimeout(() => this.fail('Python could not finish loading. Check the connection and try again.'), 60_000);
      worker.onmessage = ({ data }: MessageEvent<WorkerResponse>) => {
        if (worker !== this.worker) return;
        if (data.type === 'ready') {
          this.clearTimer();
          this.rejectReady = null;
          resolve();
        } else if (data.type === 'initialization-error') {
          this.fail(`Python could not load: ${data.error}. Try Run again.`);
        } else if (data.type === 'result' && data.id === this.pending?.id) {
          this.finish(data.result);
        }
      };
      worker.onerror = (event) => {
        if (worker !== this.worker) return;
        event.preventDefault();
        this.fail(event.message || 'The Python worker stopped unexpectedly. Try again.');
      };
      worker.postMessage({ type: 'initialize', indexURL: new URL('pyodide/', document.baseURI).href });
    });
    return this.ready;
  }

  async run(code: string, input: string, tests?: string): Promise<RunResult> {
    this.stop();
    const id = ++this.nextId;
    return new Promise<RunResult>((resolve) => {
      this.pending = { id, resolve };
      this.initialize().then(() => {
        if (this.pending?.id !== id || !this.worker) return;
        this.onStatus('running');
        // Loading time is excluded from the execution limit.
        this.timer = setTimeout(() => this.fail('Execution stopped after 10 seconds. Check for a loop that does not finish.'), 10_000);
        this.worker.postMessage({ type: 'run', id, code, input, tests });
      }).catch((error: Error) => {
        if (this.pending?.id === id) this.fail(error.message);
      });
    });
  }

  private clearTimer(): void {
    if (this.timer !== null) clearTimeout(this.timer);
    this.timer = null;
  }

  private finish(result: RunResult): void {
    this.clearTimer();
    const request = this.pending;
    this.pending = null;
    this.onStatus('idle');
    request?.resolve(result);
  }

  private fail(message: string): void {
    const reject = this.rejectReady;
    this.rejectReady = null;
    this.worker?.terminate();
    this.worker = null;
    this.ready = null;
    reject?.(new Error(message));
    this.finish({ stdout: '', stderr: '', error: message });
  }

  stop(): void {
    if (this.pending) this.fail('Execution stopped. Your code has been kept.');
  }

  dispose(): void {
    this.stop();
    this.worker?.terminate();
    this.worker = null;
    this.ready = null;
    this.clearTimer();
  }
}
