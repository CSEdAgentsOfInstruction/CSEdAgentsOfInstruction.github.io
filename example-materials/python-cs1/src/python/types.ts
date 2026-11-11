export type TestResult = { name: string; passed: boolean; message: string };
export type RunResult = {
  stdout: string;
  stderr: string;
  tests?: TestResult[];
  passed?: boolean;
  error?: string;
};

export type WorkerRequest =
  | { type: 'initialize'; indexURL: string }
  | { type: 'run'; id: number; code: string; input: string; tests?: string };
export type WorkerResponse =
  | { type: 'ready' }
  | { type: 'initialization-error'; error: string }
  | { type: 'result'; id: number; result: RunResult };
