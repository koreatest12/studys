FROM eclipse-temurin:17-jdk-alpine

# 컨테이너 로케일 설정
ENV LANG=C.UTF-8     LC_ALL=C.UTF-8
    
WORKDIR /app
COPY target/*.jar app.jar
RUN mkdir -p /app/logs /app/data && chmod -R 777 /app

# JVM 실행 시 UTF-8 강제
ENTRYPOINT ["java", "-Dfile.encoding=UTF-8", "-Dsun.jnu.encoding=UTF-8", "-jar", "app.jar"]
