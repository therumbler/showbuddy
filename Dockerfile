FROM python:3.12-slim
WORKDIR /app

EXPOSE 5019


COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

# RUN python3 -m unittest tests/*/test_*.py

ENTRYPOINT [ "./entrypoint.sh" ]
