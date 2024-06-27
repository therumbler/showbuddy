FROM python:3.12-slim
WORKDIR /app
EXPOSE 5019

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
RUN make test
ENTRYPOINT [ "./entrypoint.sh" ]