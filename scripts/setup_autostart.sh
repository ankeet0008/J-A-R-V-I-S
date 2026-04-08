#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEFAULT_PY="$PROJECT_DIR/.venv/bin/python"
PYTHON_BIN="${1:-$DEFAULT_PY}"

if [[ ! -x "$PYTHON_BIN" ]]; then
  echo "Provided Python interpreter not found or not executable: $PYTHON_BIN"
  if [[ -x "/usr/bin/python3" ]]; then
    PYTHON_BIN="/usr/bin/python3"
    echo "Falling back to: $PYTHON_BIN"
  else
    echo "No valid Python interpreter found."
    exit 1
  fi
fi

SERVICE_DIR="$HOME/.config/systemd/user"
SERVICE_FILE="$SERVICE_DIR/jarvis.service"
mkdir -p "$SERVICE_DIR"

cat > "$SERVICE_FILE" <<EOF
[Unit]
Description=JARVIS Voice Assistant
After=network.target sound.target

[Service]
Type=simple
WorkingDirectory=$PROJECT_DIR
ExecStart=$PYTHON_BIN $PROJECT_DIR/main.py
Restart=always
RestartSec=3
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable --now jarvis.service

echo "JARVIS autostart enabled."
echo "Check status with: systemctl --user status jarvis.service"
echo "View logs with: journalctl --user -u jarvis.service -f"
