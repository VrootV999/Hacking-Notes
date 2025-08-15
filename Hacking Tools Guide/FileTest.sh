#!/bin/bash

# Output file for empty Markdown files
output="empty_md_files.txt"
> "$output"  # Clear the file if it exists

# Find all .md files recursively from current directory
find "$(pwd)" -type f -name "*.md" | while read -r file; do
    # Check if file is empty or only has whitespace
    if [[ ! -s "$file" ]] || [[ -z $(grep -v '^[[:space:]]*$' "$file") ]]; then
        echo "$file" >> "$output"
    fi
done

echo "Done! List of empty Markdown files saved to $output"

