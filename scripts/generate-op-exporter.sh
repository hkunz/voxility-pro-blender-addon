#!/bin/bash

source scripts/utils.sh

VOX_OP_BASE_DIR="operators/voxel/"
FORMATS_FILE="supported-voxel-formats.txt"

if ! command -v jq &> /dev/null; then
    echo "jq is not installed. Please install it before running the script."
    exit 1
fi

JSON=$(cat "supported-voxel-formats.json")

get_usage_text() {
    echo "Usage: $0 [--all|-a|--export|-e|--import|-i] | <type> <'import' or 'export'>"
}

copy_and_modify_template() {
    local type="$1"
    local name="$2"

    code_name=$(get_code_name "$name")
    source_file="${VOX_OP_BASE_DIR}operator_{type}_${3}er.template.txt"
    destination_file="${VOX_OP_BASE_DIR}${3}ers/operator_${type}_${3}er.py"

    cp "$source_file" "$destination_file"

    sed -i "1i $(get_autogenerate_notice)" "$destination_file"
    sed -i "s/{{type}}/$type/g; s/{{name}}/$name/g; s/{{code_name}}/$code_name/g" "$destination_file"

    echo "Generated operator ${3}er $destination_file"
}

generate_op_files() {
    extensions=$(echo "$JSON" | jq -r '.[].extension')
    for type in $extensions; do
        name=$(get_vox_column_value "$type" "$JSON" "name")
        copy_and_modify_template $type "$name" "$1"
    done
}

if [ "$1" = "-e" ] || [ "$1" = "--export" ]; then
    generate_op_files "export"

elif [ "$1" = "-i" ] || [ "$1" = "--import" ]; then
    generate_op_files "import"

elif [ "$1" = "-a" ] || [ "$1" = "--all" ]; then
    generate_op_files "import"
    generate_op_files "export"

elif [ "$#" -eq 1 ] || ( [ "$#" -eq 2 ] && [[ $2 == 'import' || $2 == 'export' ]] ); then
    type="$1"
    name=$(get_vox_column_value "$type" "$JSON" "name")
    if [ -z "$name" ]; then
        echo "There is no support for voxel format '$type'."
        exit 1
    fi
    echo "Processing type: $type"
    if [ "$#" -eq 1 ]; then
        copy_and_modify_template $type "$name" "import"
        copy_and_modify_template $type "$name" "export"
    else
        copy_and_modify_template $type "$name" $2
    fi
else
    echo "$(get_usage_text)"
    exit 1
fi
