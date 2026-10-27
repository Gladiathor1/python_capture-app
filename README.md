# Capture App

A Windows desktop app (Python + PyQt5) for **activity monitoring with the user's knowledge** — for example, to provide evidence of attendance during remote work or an online exam. After the user registers their name once, the app runs from the system tray and periodically captures a webcam photo and a screenshot, then emails the collected captures as a ZIP archive.

> Only use this app on machines and with people who have clearly agreed to be monitored. Recording someone's screen or webcam without consent may be illegal.

## How it works

1. **First launch** — a form asks for first name, last name and date of birth. These are saved to `username.txt`, and captures are stored in a folder named `LastName.FirstName.DOB`.
2. **System tray** — the app minimises to the tray with *Show*, *Hide* and *Exit* options, and shows who is signed in.
3. **Capture every 5 minutes** — the app saves:
   - a webcam photo (it automatically finds the first working camera)
   - a full-desktop screenshot
4. **Upload every 5 hours** — the capture folder is zipped and emailed over SMTP, then the local files are deleted.
5. **Event log** — `Event.txt` in the capture folder records problems (webcam not connected or unplugged, screenshot failure, connection error) and when the user closed the app.

## Files

| File | Description |
| --- | --- |
| `CaptureApp.py` | The application |
| `testing.py` | Small PyQt5 experiment with a minimise-to-tray window |
| `logo.jpeg`, `logo1.ico` | App and tray icons |

## Requirements

- Windows (paths use `\`)
- Python 3.8+
- `PyQt5`, `opencv-python`, `pyautogui`

```bash
pip install PyQt5 opencv-python pyautogui
```

## Configuration

Set the SMTP sender account, password and recipient in `sendmail()` in `CaptureApp.py` — ideally loaded from environment variables rather than written in the code. The default SMTP server is `smtp.ionos.com:587`. The capture interval (`QThread.sleep(300)`) and upload interval (`QThread.sleep(18000)`) can be changed in the same file.

## Run

```bash
python CaptureApp.py
```

To package it as a standalone `.exe`:

```bash
pip install pyinstaller
pyinstaller --noconsole --onefile --icon=logo1.ico CaptureApp.py
```

Copy `logo.jpeg` next to the executable.
