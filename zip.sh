#!/bin/bash

parent_folder=$(basename "$(pwd)")
current_branch=$(git symbolic-ref -q --short HEAD || git describe --tags --exact-match)
output=$(echo "${parent_folder}-${current_branch}.zip" | tr '_' '-') 

cd ..

find . -type f -name "*.zip" -exec rm -f {} +

echo "|$parent_folder|"
echo "|$current_branch|"
echo "|$output|"

zip -r "${output}" "${parent_folder}"/* \
  --exclude "$parent_folder/.vscode/*" \
  --exclude "$parent_folder/.git/*" \
  --exclude "$parent_folder/temp/*" \
  --exclude "$parent_folder/__pycache__/*" \
  --exclude "$parent_folder/$(basename "$0")"
