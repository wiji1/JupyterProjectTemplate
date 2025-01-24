import subprocess
import webbrowser
import os
import sys
from pathlib import Path
import shutil


def render_and_open(notebook_name):
    if not notebook_name.endswith(('.ipynb', '.qmd')):
        print(f"Error: File '{notebook_name}' is not a Quarto-compatible notebook!")
        sys.exit(1)

    output_dir = Path('../html')
    output_dir.mkdir(exist_ok=True)

    # Setup paths
    input_path = Path(notebook_name)
    temp_output = input_path.with_suffix('.html')
    final_output = output_dir / temp_output.name

    try:
        result = subprocess.run(
            [
                "quarto", "render", notebook_name,
                "--to", "html",
                "--embed-resources"
            ],
            capture_output=True,
            text=True,
            check=True
        )
        print("Render notebook:", result.stdout)

        if temp_output.exists():
            shutil.move(str(temp_output), str(final_output))
        else:
            print(f"Error: Generated HTML file '{temp_output}' not found!")
            sys.exit(1)

        file_url = f"file://{os.path.abspath(final_output)}"

        print(f"Opening {file_url} in browser...")
        webbrowser.open(file_url)

    except subprocess.CalledProcessError as e:
        print("Error running quarto render:", e)
        print("Error details:", e.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Error: No file specified!")
        sys.exit(1)

    notebook_name = sys.argv[1]
    render_and_open(notebook_name)