FROM maven:3.9-eclipse-temurin-17 AS build
WORKDIR /app

# Copy root pom
COPY pom.xml .
RUN mvn -N install

# Copy common module
COPY backend/common/pom.xml backend/common/
COPY backend/common/src backend/common/src

# Copy auth module
COPY backend/auth-service/pom.xml backend/auth-service/
COPY backend/auth-service/src backend/auth-service/src

# Build common first
RUN mvn -f backend/common/pom.xml install -DskipTests

# Build auth service
RUN mvn -f backend/auth-service/pom.xml package -DskipTests

# Run stage
FROM eclipse-temurin:17-jre
WORKDIR /app
COPY --from=build /app/backend/auth-service/target/*.jar app.jar
EXPOSE 8081
ENTRYPOINT ["java", "-jar", "app.jar"]
