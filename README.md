![1780823969374](images/pipulse-banner.png)

# PiPulse: *Monitor Raspberry Pi at all times without SSH*

### Table of Contents

* [Overview](#overview)
* [How it Works](#how-it-works)
* [Features](#features)
* [Client Setup](#client-setup)
* [Agent Setup](pipulse-agent/README.md)
* [Usage](#usage)
  * [Main Command Options](#main-command-options)
  * [Endpoints](#endpoints)

## Overview

If you are running a server or even multiple on your Raspberry Pi, constant monitoring is important to make sure everything is operating smoothly and not burning through your system's resources. This is normally done by SSHing into the system to make sure processes are running as expected, but this can be a bit tedious when you just want a quick glance at certain stats or are on another device and need authentication. PiPulse makes it easy to monitor your Raspberry Pi without the need to SSH every time.

*(P.S: Although its called PiPulse, it can work on most Linux-based systems!)*

## How it Works

* A client-side CLI connects to the agent on the Raspberry Pi via the local network.
* They both use HTTP communication methods to send data to each other.
* When a command is ran on the client, it connects to the selected local IP and port (if it has the agent running).
* The agent uses `psutils` to send back system information to the client as `json` depending on the endpoint.
* The client then decodes the `json` and prints the information to the terminal.
* The data then gets inserted into the relevant tables in the `SQLite` database.

## Features

* Gather a summary of system utilization.
* Recieve detailed memory and disk information
* Stores recorded data in a `.db` file using `SQLite3`

## Client Setup

1. Go to the [releases](https://github.com/techtiki21/PiPulse/releases) tab and download the latest `pipulse-client.exe` file.
2. Open the terminal in the same directory as the `exe`.
3. Go to [Usage](#usage) or run `./pipulse-client` to view command list.

## Usage

#### Example Session

![1781856048758](images/example.gif)

#### Main Command Options


| Option                                          | Required | Description                                                            |
| ----------------------------------------------- | -------- | ---------------------------------------------------------------------- |
| `./pipulse-client`                              | YES      | Runs the CLI                                                           |
| `--host [HOST IP]`                              | YES      | Local IP of where the agent service is running                         |
| `--port [port set in the pi-agent.py script]` | NO       | Local open port of where the agent service is running (default 8000) |

#### Endpoints

After writing the main command, select an endpoint to give you the information you need.


| Endpoint | Description                                        | Arguments                                             |
| -------- | -------------------------------------------------- | ----------------------------------------------------- |
| `stats`  | Provides summary of CPU, RAM, and disk utilization | None                                                  |
| `disk`   | Provides disk space information and utilization    | None                                                  |
| `memory` | Provides RAM capacity information and utilization | None                                                  |
| `cpu`    | Provides CPU cores and core usages                 | `--seconds`: Length of recording interval (default 2) |
