#!/bin/bash

source scripts/utils.sh

RESOURCES_DIR="resources/"
DOCUMENT_CONTENT_TEMPLATE="${RESOURCES_DIR}documentation/voxility-content-test.html"
DOCUMENT_CONTENT_FINAL="${RESOURCES_DIR}documentation/voxility-content-final.html"

generate_voxility_content_final_file() {
    output_file="${DOCUMENT_CONTENT_FINAL}"
    cp "${DOCUMENT_CONTENT_TEMPLATE}" "${output_file}"
    sed -i -e '/nth-child/d' "$output_file"

    CSS=$(sed -n '/<style>/,/<\/style>/p' "$output_file" | sed '1d;$d')

        while IFS= read -r line; do
        class=$(echo "$line" | awk -F '.' '{print $2}' | sed 's/ *$//' | sed 's/ .*//')
        css=$(echo "$line" | sed 's/.*{\(.*\)}.*/\1/')
        echo Replace class=\"$class\" with style=\"$css\"
        sed -i "s/class=\"$class\"/style=\"$css\"/g" "$output_file"
    done <<< "$CSS"

    tr_tags=$(grep -o '<tr[^>]*style="[^"]*background-color:[^"]*"[^>]*>' "$output_file")
 
    awk 'BEGIN { alternate = 0; } \
        /<tr[^>]*>/ { \
            if (alternate == 0) { \
                gsub(/background-color:[^;]+;/, "background-color: #dfdfdf;", $0); \
                alternate = 1; \
            } else { \
                gsub(/background-color:[^;]+;/, "background-color: #f1f1f1;", $0); \
                alternate = 0; \
            } \
        } \
        { print }' "$output_file" > temp.html && mv temp.html "$output_file"

    sed -i -e '/<style/,/<\/style>/d' -e '/<!--.*-->/d' -e '/^\s*$/d' "$output_file"
    sed -i "1i $(get_autogenerate_notice_html)" "$output_file"
    echo "Generated file: $output_file"
}

generate_voxility_content_final_file