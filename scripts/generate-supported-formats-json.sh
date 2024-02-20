#!/bin/bash

input_file="resources/supported-voxel-formats.txt"
json_output_file="resources/supported-voxel-formats.json"

echo -n > "$json_output_file"

header_skipped=false

tail -n +3 "$input_file" | while IFS= read -r line; do
    if [ "$header_skipped" = false ]; then
        header_skipped=true
        continue
    fi

    IFS='|' read -r -a columns <<< "$line" # Split the line into columns

    # Trim leading and trailing spaces from each column
    for i in "${!columns[@]}"; do
        columns[$i]=$(echo "${columns[$i]}" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    done

    name=$(echo "${columns[0]}" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    extension=$(echo "${columns[1]}" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    loading=$(echo "${columns[2]}" | grep -q "X" && echo 1 || echo 0)
    saving=$(echo "${columns[3]}" | grep -q "X" && echo 1 || echo 0)
    thumbnails=$(echo "${columns[4]}" | grep -q "X" && echo 1 || echo 0)
    palette=$(echo "${columns[5]}" | grep -q "X" && echo 1 || echo 0)
    animations=$(echo "${columns[6]}" | grep -q "X" && echo 1 || echo 0)
    bugged=$(echo "${columns[7]}" | grep -q "X" && echo 1 || echo 0)

    json="{\"name\":\"$name\",\"extension\":\"$extension\",\"loading\":$loading,\"saving\":$saving,\"thumbnails\":$thumbnails,\"palette\":$palette,\"animations\":$animations,\"bugged\":$bugged},"

    echo "$json" >> "$json_output_file"
done

sed -i '$s/,$//' "$json_output_file"
sed -i -e '1s/^/[\n/' -e '$s/$/\n]/' "$json_output_file"
