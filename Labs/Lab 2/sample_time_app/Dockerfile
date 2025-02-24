FROM python:3.9

RUN apt-get update \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN groupadd -g 799 nyu && \
    useradd -r -u 999 -g nyu nyu

WORKDIR /app

COPY . .
RUN chown -R nyu:nyu /app

COPY requirements.txt .
RUN pip install -r requirements.txt

USER nyu

CMD ["python", "run.py"]
