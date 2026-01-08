FROM eclipse-temurin:17-jdk-alpine
WORKDIR /app
COPY target/*.jar app.jar
RUN mkdir -p /app/logs /app/data && chmod -R 777 /app
ENTRYPOINT ["java", "-jar", "app.jar"]
