#!/usr/bin/env python3
import subprocess
import webbrowser
import os
import sys
from pathlib import Path
import shutil


def render_and_open():
    # Get the notebook name from command line
    if len(sys.argv) <= 1:
        print("Error: No file specified!")
        sys.exit(1)

    notebook_name = sys.argv[1]

    # Verify it's a notebook file
    if not notebook_name.endswith(('.ipynb', '.qmd')):
        print(f"Error: File '{notebook_name}' is not a Quarto-compatible notebook!")
        sys.exit(1)

    # Create output directory if it doesn't exist
    output_dir = Path('_rendered')
    output_dir.mkdir(exist_ok=True)

    # Setup paths
    input_path = Path(notebook_name)
    temp_output = input_path.with_suffix('.html')  # This will be created in the same directory
    final_output = output_dir / temp_output.name

    try:
        # Run quarto render command (creates HTML in same directory as notebook)
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
        print("Render output:", result.stdout)

        # Move the rendered file to _rendered directory
        if temp_output.exists():
            shutil.move(str(temp_output), str(final_output))
        else:
            print(f"Error: Generated HTML file '{temp_output}' not found!")
            sys.exit(1)

        # Convert to absolute file URL
        file_url = f"file://{os.path.abspath(final_output)}"

        # Open in default browser
        print(f"Opening {file_url} in browser...")
        webbrowser.open(file_url)

    except subprocess.CalledProcessError as e:
        print("Error running quarto render:", e)
        print("Error output:", e.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    render_and_open()