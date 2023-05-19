#!/bin/sh
set -e

. /scripts/logger.sh

/scripts/wait-dependencies.sh

. ./.venv/bin/activate

log_info "Upgrade database"
python src/"${ADMINPANEL_PKG_NAME}"/manage.py migrate --noinput
echo ""

log_info "Collect static"
python src/"${ADMINPANEL_PKG_NAME}"/manage.py collectstatic --noinput
echo ""

log_info "Create superuser"
python src/"${ADMINPANEL_PKG_NAME}"/manage.py create_superuser
echo ""

/scripts/start.sh

exec "$@"
