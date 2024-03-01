#!/bin/bash

source scripts/utils.sh

RESOURCES_DIR="resources/"
DOCUMENT_CONTENT_TEMPLATE="${RESOURCES_DIR}documentation/content/voxility-content-test.html"
DOCUMENT_CONTENT_FINAL="${RESOURCES_DIR}documentation/content/voxility-content-final.html"

cleanup() {
    echo "Script interrupted. Cleaning up..."
    rm -f resources/documentation/sed* # remove temporary file created by the sed command if it is interrupted
    exit 1
}

trap cleanup INT

generate_voxility_content_final_file() {
    output_file="${DOCUMENT_CONTENT_FINAL}"
    cp "${DOCUMENT_CONTENT_TEMPLATE}" "${output_file}"
    sed -i -e '/nth-child/d' "$output_file"
    sed -i '/^[[:space:]]*\/\*/d;/^[[:space:]]*$/d' "$output_file"

    replace_class_with_style_attribute $output_file
    modify_alternate_row_colors $output_file

    sed -i -e '/<style/,/<\/style>/d' -e '/<!--.*-->/d' -e '/^\s*$/d' "$output_file"
    sed -i "1i $(get_autogenerate_notice_html)" "$output_file"
    echo "Generated file: $output_file"
}

replace_class_with_style_attribute() {
    local output_file="$1"
    CSS=$(sed -n '/<style>/,/<\/style>/p' "$output_file" | sed '1d;$d')
    while IFS= read -r line; do
        class=$(echo "$line" | awk -F '.' '{print $2}' | sed 's/ *$//' | sed 's/ .*//')
        css=$(echo "$line" | sed 's/.*{\(.*\)}.*/\1/')
        echo "Replace class=\"$class\" => style=\"${css:0:100}$(if [ ${#css} -gt 100 ]; then echo '...'; fi)\""
        sed -i "s/class=\"$class\"/style=\"$css\"/g" "$output_file"
    done <<< "$CSS"
}

modify_alternate_row_colors() {
    local output_file="$1"
    local i=0

    tr_tags=$(grep -o '<tr[^>]*style="[^"]*background-color:[^"]*background-color:[^"]*"[^>]*>.*' "$output_file")
    color=""
    while IFS= read -r tr_tag; do
        color=$(echo "$tr_tag" | grep -o 'background-color:[^;]*;' | sed -n "$(( i % 2 == 0 ? 1 : 2 ))p")
        echo "$i: use ${color} in ${tr_tag:0:100}$(if [ ${#tr_tag} -gt 100 ]; then echo '...'; fi)"
        modified_line=$(echo "$tr_tag" | sed "s/ *${color} *//")
        sed -i "s|$tr_tag|$modified_line|" "$output_file"
        ((i++))
    done <<< "$tr_tags"
}

generate_voxility_content_final_file