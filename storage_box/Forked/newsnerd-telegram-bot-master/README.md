# **NewsNerd Telegram Bot With Docker Setup To Self-hosted enthusiast**

This is a Dockerized setup for the NewsNerd Telegram Bot, which provides a simple way to get news updates from various categories in Telegram.

## **Prerequisites**

Before you begin, make sure you have the following:

- Docker installed on your machine
- Telegram Bot API token (you can obtain one by following **[these instructions](https://core.telegram.org/bots#creating-a-new-bot)**)

## **Setup**

1. Clone the repository:

```bash
git clone https://github.com/yourusername/newsnerd-telegram-bot.git
```

1. Go to the project directory:

```bash
cd newsnerd-telegram-bot
```

1. Create a **`.env`** file with your Telegram Bot API token:

```
BOT_TOKEN=<your_bot_token_here>
API_ID=<your_APP_ID>
API_HASH = <your_API_HASH>

```

1. Build the Docker image:

```docker
docker build -t newsnerd-telegram-bot .
```

1. Run the Docker container:

```docker
docker run -d --name newsnerd-telegram-bot newsnerd-telegram-bot
```

1. Start chatting with your bot on Telegram! You can use the following commands to get news updates:
- **`/news`**: get all news updates
- **`/national`**: get national news updates
- **`/business`**: get business news updates
- **`/sports`**: get sports news updates
- **`/world`**: get world news updates
- **`/politics`**: get politics news updates
- **`/technology`**: get technology news updates
- **`/startup`**: get startup news updates
- **`/entertainment`**: get entertainment news updates
- **`/miscellaneous`**: get miscellaneous news updates
- **`/science`**: get science news updates
- **`/automobile`**: get automobile news updates

## **Troubleshooting**

If you encounter any issues with the Docker setup, you can try the following:

- Check the Docker logs: **`docker logs newsnerd-telegram-bot`**
- Check the status of the Docker container: **`docker ps -a`**
- Delete the Docker container and start over: **`docker rm newsnerd-telegram-bot`** and **`docker run -d --name newsnerd-telegram-bot newsnerd-telegram-bot`**