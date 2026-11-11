"""One-time migration of copied checks; never reads or edits the source platform.

Ordinary workshop authoring does not need this script or a Python installation.
Run from this package with Python 3: python3 scripts/port-tests.py
"""
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ANNOUNCER_CHECK = '''    def test_announces_each_message_before_reading_the_next(self):
        messages = ['First', '  next  ', '', 'Go!', 'Last']
        reads = []

        def before_input(output):
            expected = [f'MESSAGE {number}: {message.upper()}'
                        for number, message in enumerate(messages[:len(reads)], start=1)]
            self.assertEqual(output, ''.join(line + '\\n' for line in expected),
                             'Announce each message before reading the next. '
                             'Put the print inside the input loop.')
            reads.append(len(reads))

        result = run_script(SCRIPT_PATH, input='\\n'.join(messages) + '\\n',
                            before_input=before_input)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(reads), 5, 'Read exactly five messages.')
        expected = [f'MESSAGE {number}: {message.upper()}'
                    for number, message in enumerate(messages, start=1)]
        self.assertEqual(result.stdout, ''.join(line + '\\n' for line in expected),
                         'Print only the five announcements.')'''


def port(path):
    source = path.read_text()
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line))

    def span(node):
        return offsets[node.lineno - 1] + node.col_offset, offsets[node.end_lineno - 1] + node.end_col_offset

    replacements = []
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and ast.unparse(node.func) == 'subprocess.run':
            command = node.args[0]
            assert isinstance(command, ast.List), path
            keywords = [k for k in node.keywords if k.arg == 'input']
            if len(command.elts) == 2:
                call = ast.Call(func=ast.Name(id='run_script'), args=[command.elts[1]], keywords=keywords)
                imports.add('run_script')
            else:
                assert len(command.elts) == 4 and ast.literal_eval(command.elts[1]) == '-c', path
                call = ast.Call(func=ast.Name(id='run_code'), args=[command.elts[2]], keywords=[
                    *keywords, ast.keyword(arg='argv', value=ast.List(elts=command.elts[3:]))])
                imports.add('run_code')
            replacements.append((*span(node), ast.unparse(call)))
        elif isinstance(node, ast.FunctionDef) and node.name == 'time_limit':
            if any(isinstance(n, ast.Attribute) and ast.unparse(n.value) == 'signal' for n in ast.walk(node)):
                start = offsets[node.decorator_list[0].lineno - 1] if node.decorator_list else span(node)[0]
                replacements.append((start, span(node)[1], ''))
                imports.add('time_limit')
        elif isinstance(node, ast.FunctionDef) and node.name == 'test_announces_each_message_before_reading_the_next':
            if 'subprocess.Popen' in ast.get_source_segment(source, node):
                start = offsets[node.lineno - 1]
                replacements.append((start, span(node)[1], ANNOUNCER_CHECK))
                imports.add('run_script')
    for start, end, text in sorted(replacements, reverse=True):
        source = source[:start] + text + source[end:]
    if imports:
        source = source.replace('import subprocess\n', '').replace('import signal\n', '')
        source = source.replace('subprocess.TimeoutExpired', 'TimeoutError')
        if 'before_input=before_input' in source:
            source = source.replace('import selectors\n', '').replace('import time\n', '')
        source = ('# Adapted for browser execution; assertions retain the original exercise contract.\n'
                  'from workshop_support import ' + ', '.join(sorted(imports)) + '\n' + source)
        ast.parse(source)
        path.write_text(source)
    return bool(imports)


if __name__ == '__main__':
    count = sum(port(path) for path in (ROOT / 'content/exercises').glob('*/tests.py'))
    print(f'Ported {count} test files to portable execution helpers.')
