import re
import os

source_file_path = 'BMAD/Archeticture'
workspace_root = '.' # Assumes the script is run from the workspace root
output_base_dir = '.' # Files will be created relative to this, matching parsed paths like 'docs/'

try:
    with open(os.path.join(workspace_root, source_file_path), 'r', encoding='utf-8') as f:
        full_content = f.read()
except FileNotFoundError:
    print(f"Error: Source file '{os.path.join(workspace_root, source_file_path)}' not found.")
    exit(1)

# Split by "Export to Sheets", keeping the delimiter temporarily to help with parsing later if needed,
# but we will mostly ignore it. We use a lookbehind to keep the content before the delimiter.
# (?=...) is a positive lookahead. We are splitting *before* "Export to Sheets".
raw_parts = re.split(r'(?=Export to Sheets)', full_content)

files_created_count = 0
errors_found = []

for i, raw_part in enumerate(raw_parts):
    if not raw_part.strip(): # Skip empty parts that might result from splitting
        continue

    # Remove the "Export to Sheets" line if it's the first line of the part, and any surrounding whitespace.
    # This handles the delimiter itself being part of the split segment.
    content_lines = raw_part.strip().splitlines()
    if content_lines and content_lines[0].strip() == "Export to Sheets":
        part_content = "\n".join(content_lines[1:]).strip()
    else:
        part_content = raw_part.strip()

    if not part_content:
        # This might happen if a part was ONLY "Export to Sheets"
        # or if the first part was empty before any actual content.
        print(f"Skipping empty content block (original part index {i}).")
        continue

    # Attempt to parse the filename from the first non-empty line of the content
    first_line_of_content = ""
    for line in part_content.splitlines():
        if line.strip():
            first_line_of_content = line.strip()
            break
    
    target_filename = None
    # A simple check if the first line looks like a filepath (e.g., ends with .md, .txt, or contains /)
    if first_line_of_content and (first_line_of_content.endswith(('.md', '.txt')) or '/' in first_line_of_content):
        # Assume the first line IS the filename. Remove it from the content to be written.
        potential_filename = first_line_of_content
        # Clean up potential non-filename characters if it's mixed with other text on the same line
        # This regex attempts to extract a path-like string
        match = re.search(r'([a-zA-Z0-9_\-\/]+\.[a-zA-Z]+)', potential_filename)
        if match:
            target_filename = match.group(1)
            # Remove the filename line from the content
            part_content_lines = part_content.splitlines()
            if part_content_lines and part_content_lines[0].strip() == first_line_of_content:
                part_content = "\n".join(part_content_lines[1:]).strip()
            print(f"Parsed filename '{target_filename}' from first line: '{first_line_of_content}'")
        else:
            errors_found.append(f"Could not parse a valid filename from potential first line: '{first_line_of_content}'. Using default for part {files_created_count + 1}.")
            target_filename = f"docs/architecture_part_{files_created_count + 1}.md"
            print(f"Using default filename: {target_filename}")
    else:
        # If the first line doesn't look like a filename, generate a default one.
        # This case might occur for the very first block of text if it doesn't start with a filename.
        errors_found.append(f"First line '{first_line_of_content}' did not look like a filename. Using default for part {files_created_count + 1}.")
        target_filename = f"docs/architecture_part_{files_created_count + 1}.md" # Default to docs/ directory
        print(f"Using default filename: {target_filename}")

    # Ensure target_filename is relative to the output_base_dir
    # and handle cases where it might already include 'docs/'
    if target_filename.startswith('docs/') and output_base_dir == '.':
        # If filename already starts with docs/ and base is '.', it's fine
        final_path = os.path.join(workspace_root, target_filename)
    elif not target_filename.startswith('docs/') and output_base_dir == '.':
        # If filename does not start with docs/ and base is '.', prepend docs/
        final_path = os.path.join(workspace_root, 'docs', target_filename)
    else:
        final_path = os.path.join(workspace_root, output_base_dir, target_filename)
        
    # Create the directory if it doesn't exist
    try:
        os.makedirs(os.path.dirname(final_path), exist_ok=True)
    except OSError as e:
        errors_found.append(f"Error creating directory {os.path.dirname(final_path)}: {e}")
        print(f"Error creating directory {os.path.dirname(final_path)}: {e}")
        continue # Skip this file

    try:
        with open(final_path, 'w', encoding='utf-8') as out_f:
            out_f.write(part_content)
        print(f"Successfully wrote: {final_path}")
        files_created_count += 1
    except IOError as e:
        errors_found.append(f"Error writing file {final_path}: {e}")
        print(f"Error writing file {final_path}: {e}")

print(f"\nScript finished. Created {files_created_count} files.")
if errors_found:
    print("\nErrors encountered during processing:")
    for err in errors_found:
        print(f"- {err}") 