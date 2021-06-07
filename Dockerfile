FROM python:3.8

WORKDIR /app
RUN mkdir -p src
COPY .env.prod bot.py requirements.txt /app/
COPY src/ /app/src
RUN rm -f /app/src/data/store/*

RUN python3.8 -m pip config set global.index-url https://mirrors.aliyun.com/pypi/simple
RUN python3.8 -m pip install --upgrade pip
RUN python3.8 -m pip install -r requirements.txt

CMD ["nb", "run"]