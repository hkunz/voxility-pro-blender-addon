#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <format_type> <name>"
    exit 1
fi

# Capture arguments
format_type="$1"
name="$2"

# Convert name to lowercase and replace spaces with underscores
code_name=$(echo "$name" | tr '[:upper:]' '[:lower:]' | tr ' ' '_')

# Set the source and destination filenames
source_file="operator_{type}_exporter.template.txt"
destination_file="operator_${format_type}_exporter.py"

# Copy the source file to the destination
cp "$source_file" "$destination_file"

# Replace placeholders in the destination file using sed
sed -i "s/{{type}}/$format_type/g; s/{{name}}/$name/g; s/{{code_name}}/$code_name/g" "$destination_file"

echo "File copied and modified successfully. New file: $destination_file"
