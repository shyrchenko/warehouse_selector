FROM python:3.11

COPY ./requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt && rm ./requirements.txt

COPY ./tests ./tests

CMD ["pytest", "./tests"]
