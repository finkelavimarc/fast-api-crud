FROM python:3.9.4-slim


WORKDIR /app
COPY . .
RUN pip install -r ./requirements.txt
EXPOSE 8081