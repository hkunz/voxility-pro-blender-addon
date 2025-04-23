#!/bin/bash

source scripts/utils.sh

UI_DIR="ui/"
VOX_OP_BASE_DIR="operators/voxel/"
VOX_FORMATS_MENU_TEMPLATE="voxel_formats_menu.py.template.txt"
JSON=$(cat "resources/supported-voxel-formats.json")

generate_voxel_formats_menu_py_file() {
    template_file="${UI_DIR}${VOX_FORMATS_MENU_TEMPLATE}"
    output_file="${UI_DIR}voxel_formats_${1}_menu.py"
    class_prefix="$(echo "$1" | tr '[:lower:]' '[:upper:]')_OT_"
    imports_content=""
    classes_content=""

    cp "$template_file" "$output_file"

    extensions=$(echo "$JSON" | jq -r '.[].extension')
    voxel_formats_list_first_item="(\"NONE\", \"None\", \"No specific target format. Only voxelize within this application.\")"
    voxel_formats_list="\n${TAB}FORMATS: List[Tuple[str, str, str]] = [\n${TAB}${TAB}${voxel_formats_list_first_item},"

    for type in $extensions; do
        name=$(get_vox_column_value "$type" "$JSON" "name")
        code_name=$(get_code_name "$name")

        import_path="voxelity_pro.$(echo ${VOX_OP_BASE_DIR}${1}ers/ | sed 's/\//./g')operator_${type}_${1}er"
        module="${class_prefix}${code_name}"
        imports_content+="from ${import_path} import ${module}\n"
        load=$(get_vox_column_value "$type" "$JSON" "loading")
        save=$(get_vox_column_value "$type" "$JSON" "saving")
        bugged=$(get_vox_column_value "$type" "$JSON" "bugged")
        if [ "$bugged" == '1' ]; then
            continue
        fi
        if ([ "$1" == 'export' ] && [ "$save" == '1' ]) || ([ "$1" == 'import' ] && [ "$load" == '1' ]); then
            classes_content+="${TAB}${class_prefix}${code_name},\n"
            voxel_formats_list+="\n${TAB}${TAB}(\"$(echo ${type} | tr '[:lower:]' '[:upper:]')\", \"${type} (${name})\", \"Target format: *.${type}\"),"
        fi
    done

    voxel_formats_list+="\n${TAB}]\n"
    voxel_formats_list+="\n${TAB}PREFERENCES_FORMATS: List[Tuple[str, str, str]] = [\n${TAB}${TAB}${voxel_formats_list_first_item},"
    voxel_formats_list+="\n${TAB}] # list is populated by AddonPreferences"

    sed -i " \
        s/{{imports}}/$imports_content/; \
        s/{{classes}}/$classes_content/" \
        "$output_file"
    sed -i "s/{{voxel_formats_list}}/${voxel_formats_list}/" "$output_file"
    sed -i "s/{{menu_class}}/VoxelFormats${1^}Menu/g" "$output_file"
    sed -i "s/{{import-export}}/${1}/g" "$output_file"
    sed -i "s/{{vox-class}}/${class_prefix}magicavoxel/g" "$output_file"
    sed -i "1i $(get_autogenerate_notice)" "$output_file"
    echo "Generated file: $output_file"
}

if [ "$1" = 'import' ] || [ "$1" = 'export' ]; then
    generate_voxel_formats_menu_py_file $1
else
    generate_voxel_formats_menu_py_file "import"
    generate_voxel_formats_menu_py_file "export"
fi