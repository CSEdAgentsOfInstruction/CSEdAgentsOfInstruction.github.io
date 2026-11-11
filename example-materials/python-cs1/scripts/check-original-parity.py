"""Maintainer-only comparison with original course checks; not needed to run the app.

Usage: python3 scripts/check-original-parity.py --source ../introcs
Only selected test files are read. All execution happens in temporary directories.
"""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--source', type=Path, required=True)
args = parser.parse_args()
manifest = json.loads((root / 'extraction-manifest.json').read_text())
results = []

for exercise in manifest['exercises']:
    folder = root / 'content/exercises' / exercise['id']
    if not (folder / 'tests.py').exists():
        continue
    original = args.source / exercise.get('files', str(Path(exercise['source']).parent)) / 'test/test.py'
    with tempfile.TemporaryDirectory(prefix='workshop-parity-') as temporary:
        shutil.copy2(original, Path(temporary) / 'test.py')
        shutil.copy2(folder / 'solution.py', Path(temporary) / 'main.py')
        try:
            result = subprocess.run([sys.executable, '-B', 'test.py'], cwd=temporary,
                                    capture_output=True, text=True, timeout=20)
            passed = result.returncode == 0
            output = result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            passed, output = False, 'Original checks timed out.'
        results.append({'id': exercise['id'], 'passed': passed, 'output': output})
        if not passed:
            print(exercise['id'], output)
    if len(results) % 10 == 0:
        print(f'Compared {len(results)} reference solutions with original CPython checks.')

(root / '.qa').mkdir(exist_ok=True)
(root / '.qa/original-parity.json').write_text(json.dumps(results, indent=2) + '\n')
print(f"{sum(r['passed'] for r in results)}/{len(results)} references pass the original checks.")
sys.exit(0 if all(r['passed'] for r in results) else 1)
