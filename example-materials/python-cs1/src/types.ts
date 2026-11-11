export interface Lesson {
  id: string;
  part: number;
  order: number;
  title: string;
  body: string;
}

export interface Choice {
  id: string;
  text: string;
  correct: boolean;
  explanation: string;
}

export interface Exercise {
  id: string;
  type: 'mcq' | 'python';
  title: string;
  prompt: string;
  part: number;
  multiple?: boolean;
  options?: Choice[];
  starter?: string;
  tests?: string;
  solution?: string;
}

export interface Draft {
  starter: string;
  code: string;
  input: string;
  completed: boolean;
  revision?: string;
}
