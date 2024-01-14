#!/bin/bash

parent_folder=$(basename "$(pwd)")
cd ..

rm -f "$parent_folder.zip"

zip -r "$parent_folder.zip" "$parent_folder"/* \
  --exclude "$parent_folder/.vscode/*" \
  --exclude "$parent_folder/.git/*" \
  --exclude "$parent_folder/$(basename "$0")"
