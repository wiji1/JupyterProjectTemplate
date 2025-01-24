import os
from pathlib import Path
import jupytext
import subprocess


def run_git_command(command, cwd=None):
    try:
        result = subprocess.run(command, cwd=cwd, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e}")
        return None


def sync_notebook_folders():
    script_dir = Path(__file__).resolve().parent
    source_folder = script_dir.parent / 'src'
    notebook_folder = script_dir.parent / 'notebooks'

    source_folder.mkdir(parents=True, exist_ok=True)
    notebook_folder.mkdir(parents=True, exist_ok=True)

    source_files = {f.stem for f in source_folder.glob('*.py')}
    notebook_files = {f.stem for f in notebook_folder.glob('*.ipynb')}

    to_convert = source_files.symmetric_difference(notebook_files)
    for filename in to_convert:
        source_path = source_folder / f'{filename}.py'
        notebook_path = notebook_folder / f'{filename}.ipynb'

        if source_path.exists() and not notebook_path.exists():
            notebook = jupytext.read(str(source_path))
            jupytext.write(notebook, str(notebook_path))
            print(f"Created notebook: {notebook_path}")

        if notebook_path.exists() and not source_path.exists():
            notebook = jupytext.read(str(notebook_path))
            jupytext.write(notebook, str(source_path))
            print(f"Created source file: {source_path}")
            run_git_command(['git', 'add', str(source_path)])

    for filename in source_files.intersection(notebook_files):
        source_path = source_folder / f'{filename}.py'
        notebook_path = notebook_folder / f'{filename}.ipynb'

        source_mtime = source_path.stat().st_mtime
        notebook_mtime = notebook_path.stat().st_mtime

        if source_mtime > notebook_mtime:
            notebook = jupytext.read(str(source_path))
            jupytext.write(notebook, str(notebook_path))
            print(f"Updated notebook: {notebook_path}")
        elif notebook_mtime > source_mtime:
            notebook = jupytext.read(str(notebook_path))
            jupytext.write(notebook, str(source_path))
            print(f"Updated source file: {source_path}")
            run_git_command(['git', 'add', str(source_path)])


if __name__ == '__main__':
    sync_notebook_folders()
