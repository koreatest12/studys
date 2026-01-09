FROM node:22-alpine
RUN apk add --no-cache openjdk17-jre
WORKDIR /app
COPY n8n_integration/n8n_source /app/n8n
COPY target/*.jar app.jar
ENTRYPOINT ["java", "-jar", "app.jar"]
