FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY app.py index.html ./
RUN mkdir /app/data && chown 10001:10001 /app/data
USER 10001:10001
EXPOSE 8080
CMD ["python", "app.py"]
