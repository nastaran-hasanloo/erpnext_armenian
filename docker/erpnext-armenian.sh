#!/usr/bin/env bash
# Run ERPNext + Frappe HR v16 in Armenian on Linux or macOS.
#   ./erpnext-armenian.sh           start (builds the image the first time)
#   ./erpnext-armenian.sh stop      stop, data is kept
#   ./erpnext-armenian.sh update    rebuild after pulling new translations
#   ./erpnext-armenian.sh reset     delete the test site and all its data
set -u
cd "$(dirname "$0")"
say() { printf '\033[36m[ERPNext-hy]\033[0m %s\n' "$*"; }
die() { printf '\033[31m[ERPNext-hy]\033[0m %s\n' "$*"; exit 1; }

command -v docker >/dev/null || die "Docker isn't installed. Get it from https://docs.docker.com/get-docker/ and run this again."
docker info >/dev/null 2>&1 || die "Docker is installed but not running. Start it and try again."
mkdir -p logs

case "${1:-start}" in
  stop)  docker compose stop; say "Stopped. Your data is still there."; exit 0 ;;
  reset) read -r -p "This deletes the test site and ALL its data. Type YES to continue: " a
         [ "$a" = "YES" ] && docker compose down -v && say "Done. Run ./erpnext-armenian.sh for a fresh site."; exit 0 ;;
  update) REBUILD=1 ;;
  start) REBUILD=0 ;;
  *) die "Unknown command: $1 (use start, stop, update or reset)" ;;
esac

if [ "$REBUILD" = 1 ] || [ -z "$(docker images -q erpnext-armenian:v16)" ]; then
  say "Building the image. The first time takes 20-40 minutes and downloads about 3 GB."
  docker compose build backend 2>&1 | tee logs/build.log
  [ "${PIPESTATUS[0]}" = 0 ] || die "Build failed. Please open an issue and attach docker/logs/build.log."
fi

say "Starting containers..."
docker compose up -d 2>&1 | tee logs/up.log || die "Couldn't start. Attach docker/logs/up.log to an issue."

say "Waiting for the site (first time: 5-15 minutes)..."
for _ in $(seq 180); do
  s=$(docker compose ps -a --format '{{.State}} {{.ExitCode}}' create-site)
  case "$s" in "exited 0"*) break ;; "exited "*) docker compose logs create-site > logs/create-site.log; die "Site setup failed. Attach docker/logs/create-site.log to an issue." ;; esac
  sleep 10; printf '.'
done; echo
for _ in $(seq 60); do curl -fs -o /dev/null http://localhost:8080/login && break; sleep 5; done

# Older test sites: make sure the app is installed, then refresh.
docker compose exec -T backend bench --site frontend list-apps 2>/dev/null | grep -q erpnext_armenian || \
  docker compose exec -T backend bench --site frontend install-app erpnext_armenian 2>&1 | tee logs/install-app.log
docker compose exec -T backend bench --site frontend migrate > logs/migrate.log 2>&1
docker compose exec -T backend bench --site frontend clear-cache >/dev/null

say "Ready: http://localhost:8080  (user Administrator, password admin, local testing only)"
(command -v xdg-open >/dev/null && xdg-open http://localhost:8080) || (command -v open >/dev/null && open http://localhost:8080) || true
