#!/bin/bash

source scripts/utils.sh

UI_DIR="ui/"
ADDON_PREFERENCES_TEMPLATE="addon_preferences.py.template.txt"
JSON=$(cat "resources/supported-voxel-formats.json")

generate_addon_preferences_py_file() {
    template_file="${UI_DIR}${ADDON_PREFERENCES_TEMPLATE}"
    output_file="${UI_DIR}addon_preferences.py"

    check_content=""
    properties_content=""
    layout_content=""

    cp "$template_file" "$output_file"

    extensions=$(echo "$JSON" | jq -r '.[].extension')

    for type in $extensions; do
        name=$(get_vox_column_value "$type" "$JSON" "name")
        code_name=$(get_code_name "$name")
        load=$(get_vox_column_value "$type" "$JSON" "loading")
        save=$(get_vox_column_value "$type" "$JSON" "saving")
        bugged=$(get_vox_column_value "$type" "$JSON" "bugged")
        if [ "$bugged" == '1' ]; then
            continue
        fi
        if [ "$save" == '1' ] || [ "$load" == '1' ]; then
            check_content+="\n${TAB}if self.type_${type}:"
            check_content+="\n${TAB}${TAB}pass"
            properties_content+="${TAB}type_${type}: bpy.props.BoolProperty(\n"
            properties_content+="${TAB}${TAB}name=\"*.${type} (${name})\",\n"
            properties_content+="${TAB}${TAB}default=True,\n"
            properties_content+="${TAB}${TAB}update=update_bool_property,\n"
            properties_content+="${TAB}) # type: ignore\n\n"
            layout_content+="\n${TAB}${TAB}box.prop(self, \"type_${type}\")"
        fi
    done

    sed -i " \
        s/{{check}}/$check_content/; \
        s/{{properties}}/$properties_content/; \
        s/{{layout}}/$layout_content/" \
        "$output_file"

    sed -i "1i $(get_autogenerate_notice)" "$output_file"
    echo "Generated file: $output_file"
}

generate_addon_preferences_py_file