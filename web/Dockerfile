FROM python:3.9-alpine
EXPOSE 5000
WORKDIR /app
COPY requirements.txt .
RUN pip install -r ./requirements.txt
COPY src/ .
RUN chmod +x ./entrypoint.sh
CMD ["./entrypoint.sh"]