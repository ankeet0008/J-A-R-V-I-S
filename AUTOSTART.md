# JARVIS Autostart (Linux)

Use this when you want JARVIS to launch automatically on login.

## 1) Create a virtual environment (recommended)

```bash
cd /home/ankeet/Downloads/J-A-R-V-I-S-main
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

## 2) Enable autostart service

```bash
chmod +x scripts/setup_autostart.sh
./scripts/setup_autostart.sh /home/ankeet/Downloads/J-A-R-V-I-S-main/.venv/bin/python
```

## 3) Useful service commands

```bash
systemctl --user status jarvis.service
journalctl --user -u jarvis.service -f
systemctl --user restart jarvis.service
systemctl --user disable --now jarvis.service
```

## Notes

- This is a user-level service and starts when you log in.
- For microphone access, make sure your Linux audio stack and permissions are configured.
- If you use GNOME/KDE and want startup after desktop session is ready, this approach is usually reliable.
