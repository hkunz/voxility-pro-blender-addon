#!/bin/zsh

EXIT_CODE_SUCCESS=0
EXIT_CODE_ERROR_EXECUTING_VOXCONVERT=10
EXIT_CODE_ERROR_UNSUPPORTED_ARCH=11 # Error code on mac when architecuture is other than arm64 or x86_64
EXIT_CODE_ERROR_ROSETTA_NOT_INSTALLED=12 # Error code on mac arm64 architecture

get_formatted_args() {
    local command_str="$1"
    local vox_index=$(echo "$command_str" | grep -b -o 'vox' | cut -d: -f1)
    if [[ -z "$vox_index" ]]; then
        echo "No 'vox' found in command string."
        return
    fi
    local command_sub_str="${command_str:${vox_index}}"
    local split_args=(${(s/ --/ # )command_sub_str})
    unset split_args[1] # Remove the first argument as it is the command itself

    echo "${split_args[@]}" | tr ' #' '\n' # Join arguments with newlines
}

command="$1"
command_str="$2"
arch_type=$(uname -m)

echo "Execute command on '$arch_type' architecture: $command_str"

if [[ "$arch_type" == "x86_64" ]]; then
    eval "$command_str"
elif [[ "$arch_type" == "arm64" ]]; then
    if command -v arch >/dev/null 2>&1; then
        eval "arch -x86_64 $command_str"
    else
        echo "You need to install 'Rosetta 2' to run binaries of 'x86_64' on '$arch_type'. See 'https://apple.stackexchange.com/questions/408375/zsh-bad-cpu-type-in-executable' on how to install Rosetta 2" >&2
        exit $EXIT_CODE_ERROR_ROSETTA_NOT_INSTALLED
    fi
else
    echo "Unsupported architecture: '$arch_type'" >&2
    exit $EXIT_CODE_ERROR_UNSUPPORTED_ARCH
fi

if [[ $? -eq 0 ]]; then
    exit $EXIT_CODE_SUCCESS
fi

printf "\nExecuted command:\n" >&2
echo "${command_str}" >&2

exit $EXIT_CODE_ERROR_EXECUTING_VOXCONVERT
