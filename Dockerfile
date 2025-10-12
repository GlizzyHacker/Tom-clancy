FROM python:3.13

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ARG discord_token=token
ARG webhook_url
ENV DISCORD_API_TOKEN=${discord_token}
ENV LOG_WEBHOOK_URL=${webhook_url}
ENV FOREVER_WEBHOOK_URL=${critical_webhook_url}

CMD [ "python", "./forever.py", "\"-u ./main.py\"" ]
