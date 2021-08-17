FROM python:3.9

WORKDIR /app
RUN mkdir -p src
COPY .env.prod bot.py requirements.txt /app/
COPY src/ /app/src
RUN rm -f /app/src/data/store/*
RUN rm -f /app/src/data/auth/*

#RUN python3 -m pip config set global.index-url https://mirrors.aliyun.com/pypi/simple
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --use-deprecated=legacy-resolver -r requirements.txt

ENTRYPOINT ["nb", "run"]
