FROM node:20-alpine
RUN apk add --no-cache openjdk17-jre git
WORKDIR /app
COPY n8n_integration/n8n_source /app/n8n
COPY target/*.jar app.jar
RUN mkdir -p /app/logs /app/data && chmod -R 777 /app
# 실행 예시 (Java 앱 실행)
ENTRYPOINT ["java", "-jar", "app.jar"]
