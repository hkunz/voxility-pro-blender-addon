#!/bin/bash

vox_exporter_version=$(grep -oP '"version": \(([^)]+)\),' __init__.py | sed 's/[^0-9]//g' | tr -d '\n' | sed 's/\(.\)/\1./g' | sed 's/\.$//')
voxconvert_version=$(cat "__init__.py" | sed -n 's/.* voxconvert-\([0-9]\+\.[0-9]\+\.[0-9]\+\) .*/\1/p')

echo "Vox Exporter version: ${vox_exporter_version}"
echo "Vengi-voxconvert version: ${voxconvert_version}"

parent_folder=$(basename "$(pwd)")
current_branch=$(git symbolic-ref -q --short HEAD || git describe --tags --exact-match)
output_zip=$(echo "${parent_folder}-${current_branch}.zip" | tr '_' '-')

cd ..

find . -type f -name "*.zip" -exec rm -f {} +

echo "Parent: $parent_folder"
echo "Branch: $current_branch"
echo "Output: $output_zip"

vox_exe_dir="${parent_folder}/voxconvert-executable/${voxconvert_version}"

if [ ! -d "$vox_exe_dir" ]; then
  echo "Error: No vox executable dir ${vox_exe_dir} found."
  exit 1
fi

zip_cmd="zip -r '${output_zip}' '${parent_folder}'/* \
  --exclude "$parent_folder/.vscode/*" \
  --exclude "$parent_folder/.git/*" \
  --exclude "$parent_folder/temp/*" \
  --exclude "$parent_folder/*.sh" \
  --exclude "$parent_folder/*.template.*" \
  --exclude "$parent_folder/$(basename "$0")" \
"

mapfile -t exclude_pycache < <(find "${parent_folder}" -type d -name "__pycache__")
mapfile -t exclude_executables < <(find "${parent_folder}/voxconvert-executable" -mindepth 1 -maxdepth 1 -type d -not -name "${voxconvert_version}")
exclude_paths=("${exclude_executables[@]}" "${exclude_pycache[@]}")

for path in "${exclude_paths[@]}"; do
  zip_cmd+=" --exclude \"$path/*\""
done

eval "$zip_cmd"

echo "Created zip file: $(pwd)/${output_zip}"
