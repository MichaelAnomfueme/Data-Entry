FROM python:3.9-slim-buster

WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy source code
COPY . .

# Set environment variables
ENV API_ID=<YOUR_API_ID>
ENV API_HASH=<YOUR_API_HASH>
ENV BOT_TOKEN=<YOUR_BOT_TOKEN>

# Start the bot
CMD ["python", "news_bot.py"]
