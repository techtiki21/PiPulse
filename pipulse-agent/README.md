# PiPulse Agent Setup

* [Overview](#overview)
* [Setup](#setup)
* [Monitoring](#monitoring)

## Overview

The PiPulse Agent is a systemd service that will run in the background of your Raspberry Pi while being extremely lightweight, not requiring a lot of system resources and demand. I will go though how to setup the Python virtual environment, edit the .service file for your system, and monitor its status after it has been setup.

## Setup

*Make sure your Pi has Python 3 installed. (or higher)*

Open a terminal window in the `pipulse-agent` folder.

#### Edit Port (Optional)

1. Open `pi-agent.py`
2. Modify the `PORT` variable to a oprt of your choosing. (anything below port 1000 is not recommended)

#### Setup Virtual Environment

1. Create a virtual environment: `python -m venv .venv`
2. Activate it: `source .venv/bin/activate`
3. Install Python dependencies: `pip install -r requirements.txt`

#### Modify .service file, open local port, and add to daemon

1. Open `pipulse-agent.service` on a text editor of your choice.
2. Replace everything in curly braces with the necessary values.
3. Save it and move it to `/etc/systemd/system/` (sudo may be needed)
4. If you have `ufw` installed, make sure to open the port locally: `sudo ufw allow [port]`. Otherwise, skip this step.

#### Refresh Daemon and Start Service

1. Reload the daemon: `sudo systemctl daemon-reload`
2. Start the service: `sudo systemctl start pipulse-agent.service`
3. Verify it's running: `sudo systemctl status pipulse-agent.service`

## Monitoring

Once the service is running, you won't even be able to tell! However, that doesn't mean it's just going to run forever with no way to stop it. You can modify it's behavior and monitor it's status to make sure its running correctly.


| Action                           | Command                                        | Information                                                                                            |
| -------------------------------- | ---------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| Set service to startup on reboot | `sudo systemctl enable pipulse-agent.service`  | You can also turn it off by replacing`enable` with `disable`                                           |
| Restart service                  | `sudo systemctl restart pipulse-agent.service` | This command can be used to quickly reload the service if a change has been made to the Python script. |
| View service logs                | `sudo journalctl -u pipulse-agent.service`     | Adding`-f` to the end will give you real-time logs; great for debugging.                              |
