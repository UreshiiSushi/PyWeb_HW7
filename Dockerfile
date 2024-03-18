FROM python:alpine3.19

ENV APP /pyweb_hw7

WORKDIR ${APP}

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5432

ENTRYPOINT [ "python", "main.py" ]