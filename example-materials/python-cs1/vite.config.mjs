import { defineConfig, normalizePath } from 'vite';
import { createRequire } from 'node:module';
import { dirname, resolve } from 'node:path';
import { mkdirSync, copyFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const require = createRequire(import.meta.url);
const root = dirname(fileURLToPath(import.meta.url));
const contentRoot = normalizePath(resolve(root, 'content')) + '/';

function preparePython() {
  const packageRoot = dirname(require.resolve('pyodide/package.json'));
  const target = resolve(root, 'public/pyodide');
  mkdirSync(target, { recursive: true });
  for (const name of ['pyodide.mjs', 'pyodide.asm.mjs', 'pyodide.asm.wasm', 'python_stdlib.zip', 'pyodide-lock.json']) {
    copyFileSync(resolve(packageRoot, name), resolve(target, name));
  }
}

export default defineConfig({
  base: './',
  plugins: [{
    name: 'workshop-content-and-python',
    buildStart: preparePython,
    configureServer(server) {
      preparePython();
      server.watcher.add(resolve(root, 'content'));
      const reload = (file) => {
        if (normalizePath(file).startsWith(contentRoot)) {
          server.ws.send({ type: 'full-reload' });
        }
      };
      server.watcher.on('add', reload);
      server.watcher.on('unlink', reload);
    },
    handleHotUpdate({ file, server }) {
      if (normalizePath(file).startsWith(contentRoot)) {
        server.ws.send({ type: 'full-reload' });
        return [];
      }
    },
  }],
  build: { target: 'es2022' },
});
