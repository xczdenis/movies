#!/bin/bash


. ./scripts/utils.sh
. ./scripts/colors.sh

run_command_with_logs() {
    header=$(trim ${1})
    command=$(trim ${2})

    echo "[= ${color_blue}${header}${color_reset} =]"
    echo "${color_yellow}run command: ${color_purple}${command}${color_reset}"
    ${command} || true
    echo ""
}
