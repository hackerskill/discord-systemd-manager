# discord-systemd-manager
A Discord bot for managing systemd services on Linux servers directly from Discord.

## Features

* **Automatic Service Discovery** — Automatically detects systemd services following the `user-` naming convention.
* **Service Status** — Check current status of a service.
* **Start Services** — Start a systemd service.
* **Stop Services** — Stop a systemd service.
* **Restart Services** — Restart a systemd service.
* **Service Logs** — View recent logs of a service.
* **Service Selection** — Select services using Discord's built-in dropdown menus.
* **Slash Commands** — Manage services using simple Discord slash commands.
* **Systemd Integration** — Uses `systemctl` and `journalctl` to interact directly with systemd.
* **Bot Information** — View information about the systemd manager bot.

## Slash Commands
* **`services`** — Fetches a list of all services on the server along with their current state.
* **`status`** — View status of a specific service.
* **`start`** — Start a service.
* **`restart`** — Restart a service.
* **`stop`** — Stop a service.
* **`logs`** — View logs of a specific service.
* **`ping`** — Check chatbot connectivity status.
* **`clear`** — Clear recent messages by chatbot.
* **`about`** — Shows information about the bot itself.


## Service Naming Convention

The bot automatically discovers services whose names start with `user-`.

For a service to be detected and managed by the bot, its systemd unit name must follow this naming convention:

```text
user-<service-name>.service
```

Examples:

```text
user-discord-bot.service
user-website.service
user-api.service
```

Services that do not start with `user-` are ignored by the bot.

Template services containing `@` are also ignored.

> **Important:** If a service does not follow the `user-` naming convention, it will not be discovered by the bot.


## Setup

1. Get Token for Discord bot at [Discord Developer Portal](https://discord.com/developers/).

2. Clone the repo

3. **Create and activate a virtual environment:**
   * **macOS/Linux:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   * **Windows:**
     ```bash
     python -m venv .venv
     .\.venv\Scripts\activate
     ```
4. **Change `.env.example` to `.env` with the following keys-**
    * Discord token specific for a bot

5. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

6. **Deploy on server:**

    The bot can be run as a systemd service. Before creating the service file, replace the following placeholders:
      * `your-user` — Replace with the Linux user that will run the bot and has the required permissions to manage the systemd services.
      * `/path/to/discord-systemd-manager` — Replace with the absolute path to the cloned discord-systemd-manager directory.

    Create the service file:

    ```bash
    sudo nano /etc/systemd/system/user-discord-bot.service
    ```

    Add the following configuration:

    ```ini
    [Unit]
    Description=Systemd Manager
    After=network.target

    [Service]
    User=your-user
    WorkingDirectory=/path/to/discord-systemd-manager
    ExecStart=/path/to/discord-systemd-manager/.venv/bin/python /path/to/discord-systemd-manager/main.py
    Restart=always

    [Install]
    WantedBy=multi-user.target
    ```

    Then reload systemd and enable the bot:

    ```bash
    sudo systemctl daemon-reload
    sudo systemctl enable --now user-discord-bot.service
    ```

    Check the bot's service status:

    ```bash
    systemctl status user-discord-bot.service
    ```

## Running the Application

Once setup is verified, `main.py` can be started through `systemd` to start the Discord systemd manager.

---

**Made by hackerskill**
