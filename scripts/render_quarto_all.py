import shutil
import subprocess
from pathlib import Path


def render_notebooks(notebook_dir='../notebooks'):
    notebook_dir = Path(notebook_dir)

    if not notebook_dir.is_dir():
        print(f"Error: Directory '{notebook_dir}' not found!")
        return

    output_dir = Path('../html')
    output_dir.mkdir(exist_ok=True)

    notebook_files = list(notebook_dir.glob('*.ipynb')) + list(notebook_dir.glob('*.qmd'))

    if not notebook_files:
        print("No notebook files found in the directory!")
        return

    for input_path in notebook_files:
        try:
            temp_output = input_path.with_suffix('.html')
            final_output = output_dir / temp_output.name

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
            print(f"Render notebook: {input_path.name}")

            if temp_output.exists():
                shutil.move(str(temp_output), str(final_output))
            else:
                print(f"Error: Generated HTML file '{temp_output}' not found!")

        except subprocess.CalledProcessError as e:
            print(f"Error rendering {input_path.name}:", e)
            print("Error details:", e.stderr)
        except Exception as e:
            print(f"Unexpected error processing {input_path.name}: {e}")


if __name__ == "__main__":
    render_notebooks()