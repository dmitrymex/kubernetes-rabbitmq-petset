FROM ubuntu:xenial

RUN apt update && \
    apt install -y --no-install-recommends python rabbitmq-server && \
    apt clean

COPY startup.py /sbin/

RUN echo "asecret" > /var/lib/rabbitmq/.erlang.cookie

RUN chown -R rabbitmq:rabbitmq /var/lib/rabbitmq /var/log/rabbitmq /etc/rabbitmq && \
    chmod 600 /var/lib/rabbitmq/.erlang.cookie

USER rabbitmq
