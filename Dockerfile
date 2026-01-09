FROM node:22-alpine
RUN apk add --no-cache openjdk17-jre
WORKDIR /app
COPY n8n_integration/n8n_source /app/n8n
COPY target/*.jar app.jar
# 대량 데이터 복사
COPY src/main/resources/data /app/data
ENV N8N_DATA_DIR=/app/data
ENTRYPOINT ["java", "-jar", "app.jar"]
