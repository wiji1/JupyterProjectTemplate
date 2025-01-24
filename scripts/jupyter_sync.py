import os
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
    source_folder = '../src'
    notebook_folder = '../notebooks'

    os.makedirs(source_folder, exist_ok=True)
    os.makedirs(notebook_folder, exist_ok=True)

    source_files = set(os.path.splitext(f)[0] for f in os.listdir(source_folder) if f.endswith('.py'))
    notebook_files = set(os.path.splitext(f)[0] for f in os.listdir(notebook_folder) if f.endswith('.ipynb'))

    to_convert = source_files.symmetric_difference(notebook_files)

    for filename in to_convert:
        source_path = os.path.join(source_folder, filename + '.py')
        notebook_path = os.path.join(notebook_folder, filename + '.ipynb')

        if os.path.exists(source_path) and not os.path.exists(notebook_path):
            notebook = jupytext.read(source_path)
            jupytext.write(notebook, notebook_path)
            print(f"Created notebook: {notebook_path}")


        if os.path.exists(notebook_path) and not os.path.exists(source_path):
            notebook = jupytext.read(notebook_path)
            jupytext.write(notebook, source_path)
            print(f"Created source file: {source_path}")

            run_git_command(['git', 'add', source_path])

    for filename in source_files.intersection(notebook_files):
        source_path = os.path.join(source_folder, filename + '.py')
        notebook_path = os.path.join(notebook_folder, filename + '.ipynb')

        source_mtime = os.path.getmtime(source_path)
        notebook_mtime = os.path.getmtime(notebook_path)

        if source_mtime > notebook_mtime:
            notebook = jupytext.read(source_path)
            jupytext.write(notebook, notebook_path)
            print(f"Updated notebook: {notebook_path}")

        elif notebook_mtime > source_mtime:
            notebook = jupytext.read(notebook_path)
            jupytext.write(notebook, source_path)
            print(f"Updated source file: {source_path}")
            run_git_command(['git', 'add', source_path])


if __name__ == '__main__':
    sync_notebook_folders()