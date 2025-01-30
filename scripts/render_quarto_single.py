import subprocess
import webbrowser
import os
import sys
from pathlib import Path
import shutil


def render_and_open(notebook_name):
    input_path = Path(notebook_name).resolve()
    if not input_path.exists():
        print(f"Error: File '{input_path}' does not exist!")
        sys.exit(1)

    if not input_path.suffix in ('.ipynb', '.qmd'):
        print(f"Error: File '{notebook_name}' is not a Quarto-compatible notebook!")
        sys.exit(1)

    script_dir = Path(__file__).resolve().parent
    output_dir = script_dir / '../html'
    output_dir.mkdir(exist_ok=True)

    temp_output = input_path.with_suffix('.html')
    final_output = output_dir / temp_output.name

    try:
        print(f"Rendering notebook '{input_path}' to HTML...")
        result = subprocess.run(
            [
                "quarto", "render", str(input_path),
                "--to", "html",
                "--embed-resources"
            ],
            capture_output=True,
            text=True,
            check=True
        )
        print("Render notebook output:", result.stdout)

        if temp_output.exists():
            shutil.move(str(temp_output), str(final_output))
            print(f"Rendered HTML saved to: {final_output}")
        else:
            print(f"Error: Generated HTML file '{temp_output}' not found!")
            sys.exit(1)

        file_url = final_output.as_uri()
        print(f"Opening {file_url} in browser...")
        webbrowser.open(file_url)

    except subprocess.CalledProcessError as e:
        print(f"Error running Quarto render for '{input_path}':")
        print("Command output:", e.stdout)
        print("Error details:", e.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Error: No file specified!")
        print("Usage: python scripts/render_quarto_single.py <notebook_file>")
        sys.exit(1)

    notebook_name = sys.argv[1]
    render_and_open(notebook_name)
