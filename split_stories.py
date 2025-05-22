import re
import os

source_file_path = 'BMAD/Stories'
# Assumes the script is run from the workspace root
workspace_root = '.' 

try:
    with open(os.path.join(workspace_root, source_file_path), 'r', encoding='utf-8') as f:
        full_content = f.read()
except FileNotFoundError:
    print(f"Error: Source file '{os.path.join(workspace_root, source_file_path)}' not found.")
    exit(1)

# The main file BMAD/Stories starts with "---" on the first line.
# Stories are then separated by "\n---
# File: <filepath>".
# So, we split by this pattern.
# The first element of the split will be the initial "---".
# Subsequent elements will be "<filepath>\n---\n<content_for_that_file>".

parts = re.split(r'\n---\nFile:\s*', full_content)

files_created_count = 0
errors_found = []

# Iterate from the second part (parts[1:]), as parts[0] is just the initial "---"
if len(parts) > 1:
    for part_content in parts[1:]:
        part_content = part_content.strip() # Clean up whitespace around the block
        if not part_content:
            continue

        try:
            # The part_content is now "<filepath>\n---\n<actual_content_for_new_file>"
            # Split into filepath and the rest (which is the content)
            path_and_content_list = part_content.split('\n', 1)
            target_relative_path = path_and_content_list[0].strip()
            
            if len(path_and_content_list) < 2:
                errors_found.append(f"Malformed block for inferred path '{target_relative_path}': No content found after the path line.")
                continue

            actual_content_for_file = path_and_content_list[1]
            
            # The content for the new file should start with "---"
            if not actual_content_for_file.startswith('---'):
                errors_found.append(f"Content for '{target_relative_path}' does not start with '---' as expected. Found: '{actual_content_for_file[:30].replace('\n', ' ')}...'")
                # Depending on strictness, you might choose to skip or write anyway.
                # For this script, we'll log the error and attempt to write.

            absolute_target_path = os.path.join(workspace_root, target_relative_path)
            target_dir = os.path.dirname(absolute_target_path)
            
            if target_dir and not os.path.exists(target_dir):
                os.makedirs(target_dir)
                print(f"Created directory: {target_dir}")
                
            with open(absolute_target_path, 'w', encoding='utf-8') as outfile:
                outfile.write(actual_content_for_file)
            files_created_count += 1
            print(f"Successfully wrote: {target_relative_path}")

        except Exception as e:
            errors_found.append(f"Error processing block starting with '{part_content[:60].replace('\n', ' ')}...': {str(e)}")
else:
    print("No story parts found after splitting. Check the content of BMAD/Stories and the split pattern.")

print(f"\n--- Summary ---")
print(f"Files created/updated: {files_created_count}")
if errors_found:
    print(f"Errors encountered: {len(errors_found)}")
    for err in errors_found:
        print(f"- {err}")
else:
    print("No errors encountered.") 