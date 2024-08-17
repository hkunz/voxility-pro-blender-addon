#!/bin/zsh

EXIT_CODE_SUCCESS=0
EXIT_CODE_INSTALLATION_ERROR=10

softwareupdate --install-rosetta --agree-to-license

if [[ $? -eq 0 ]]; then
    exit $EXIT_CODE_SUCCESS
fi

#echo "Installation for Rosetta 2 failed" >&2
exit $EXIT_CODE_INSTALLATION_ERROR