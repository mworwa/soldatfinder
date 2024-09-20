# SoldatFinder

https://t.me/SoldatFinderBot

A Telegram bot designed to help families and loved ones find information about missing Ukrainian soldiers by monitoring multiple Telegram channels for updates.


## Table of Contents

- [Background](#background)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [License](#license)
- [Contributing](#contributing)

## Background

In the ongoing conflict, many Ukrainian soldiers are reported missing, causing immense distress to their families and friends. Some of these soldiers may have been taken as prisoners of war, with information about them shared on various Telegram channels. However, these channels often contain graphic content and are challenging to monitor continuously.

**SoldatFinder** automates the process of scanning these channels for specific names, surnames, or birthdays. When a match is found, the bot sends a notification, providing a glimmer of hope and timely information to those waiting for news.

## Features

- **Automated Monitoring**: Continuously scans specified Telegram channels for updates about prisoners.
- **Custom Search Criteria**: Allows users to input names, surnames, and birthdays to monitor.
- **Instant Notifications**: Sends immediate alerts when matching information is found.
- **User-Friendly Interaction**: Manages conversations seamlessly through the Telegram interface.
- **Two Main Components**:
  - `bot.py`: Manages the bot's conversations with users.
  - `observer.py`: Monitors channels and searches for specified soldier data.

## Installation

### Prerequisites

- Python 3.8+
- [Telegram API ID](https://core.telegram.org/api/obtaining_api_id)
- [Telegram Bot API Token](https://core.telegram.org/bots#3-how-do-i-create-a-bot)

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/telegram-prisoner-monitor-bot.git
   cd telegram-prisoner-monitor-bot
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up enviroment variables**

   - Contact [@BotFather](https://t.me/BotFather) on Telegram.
   - Create a new bot and obtain the API token.
   - Obtain API ID https://core.telegram.org/api/obtaining_api_id
   - Update the `.env` file with your values.

## Usage

The bot operates through two main processes that need to run simultaneously.

### 1. Start the Conversation Manager

Handles interactions with users on Telegram.

```bash
python bot.py
```

### 2. Start the Observer

Monitors the specified Telegram channels for updates.

```bash
python observer.py
```
## Channels
SoldatFinder monitors this channels:
- https://web.telegram.org/a/#-1001542074211
- https://web.telegram.org/a/#-1001923497239
- https://web.telegram.org/a/#-1001666094161
- https://web.telegram.org/a/#-1001676376547
- https://web.telegram.org/a/#-1001909925694
- https://web.telegram.org/a/#-1001285348580
- https://web.telegram.org/a/#-1001837743468
- https://web.telegram.org/a/#-1001689374765
- https://web.telegram.org/a/#-1001453960815
- https://web.telegram.org/a/#-1002061108277

If you know any other channels that might contains usefull informations please create Issue
## Configuration

All configurations are managed through the `.env` file.

## License

This project is licensed under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature-name`.
3. Commit your changes: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature/your-feature-name`.
5. Submit a pull request.