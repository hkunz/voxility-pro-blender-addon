#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <version>"
    exit 1
fi

# Validate the version format (X.X.X)
if ! [[ $1 =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Invalid version format. Please use X.X.X (e.g., 1.0.0)"
    exit 1
fi

# Check if the version tag already exists
if git rev-parse -q --verify "v$1" >/dev/null; then
    echo "Tag v$1 already exists in Git. Aborting."
    exit 1
fi


IFS='.' read -r v_major v_minor v_patch <<< "$1"

tag_name="v$1"

echo "Attempting to update __init__.py to reflect the new version."

read -p "Do you want to commit this change? [y/n]: " answer

if [ "${answer,,}" != "y" ]; then
    echo "Nothing was done."
    exit 0
fi

if ! git pull --rebase; then
    echo "Error: Failed to pull changes. Aborting."
    exit 1
fi

sed -i "s/\"version\": ([0-9]\+, [0-9]\+, [0-9]\+)/\"version\": ($v_major, $v_minor, $v_patch)/g" __init__.py
git add __init__.py
git commit -m "Update version in __init__.py to $1"
git push
echo "Version change to __init__.py committed successfully."

git tag -a "$tag_name" -m "Release version $1"
git push origin "$tag_name"

echo "Tag $tag_name created and pushed successfully."