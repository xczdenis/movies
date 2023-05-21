#!/bin/bash


to_upper() {
  echo "$1" | tr '[:lower:]' '[:upper:]'
}

trim() {
    local var="$*"
    var="${var#"${var%%[![:space:]]*}"}"
    var="${var%"${var##*[![:space:]]}"}"
    echo -n "$var"
}
