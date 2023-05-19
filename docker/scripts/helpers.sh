. /scripts/colors.sh

to_upper() {
  echo "$1" | tr '[:lower:]' '[:upper:]'
}

check_service() (
  service_name=$1
  host=$2
  port=$3

  log_info "Waiting the service: ${color_white}${service_name} (url=${host}:${port})"
  /scripts/wait-for-it.sh "${host}":"${port}" -t 120 --
  log_success "${service_name} is up!${color_reset}"
  echo ""
)
