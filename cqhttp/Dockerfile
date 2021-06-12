FROM ubuntu
RUN mkdir -p /app
COPY ./config.hjson ./go-cqhttp /app/
WORKDIR /app
ENTRYPOINT ["./go-cqhttp"]