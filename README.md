# English Learning Telegram Bot

**Creator / Developer: MOEDSH**

## Runtime
- Python 3.11
- `python-telegram-bot==20.7`

## Run locally
1. Install dependencies: `pip install -r requirements.txt`
2. Set the environment variable `BOT_TOKEN` to the token from BotFather.
3. Start the bot: `python main.py`

## Deploy on Inject Cloud
1. Connect this GitHub repository (or upload this project).
2. Select Python runtime.
3. Set the startup command to `python main.py`.
4. Add an environment variable named `BOT_TOKEN` and paste your NEW Telegram bot token as its value.
5. Deploy / restart the application.

Do not put the bot token in source code or commit it to GitHub.

The MOEDSH logo is stored in `assets/moedsh_logo.png` and is sent with the `/start` welcome message.
