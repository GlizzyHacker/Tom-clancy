FROM python:3.13

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ARG discord_token=token
ENV DISCORD_API_TOKEN=${discord_token}

CMD [ "python", "./main.py" ]