FROM maven:3.9-eclipse-temurin-17 AS build
WORKDIR /app

# Copy root pom
COPY pom.xml .
RUN mvn -N install

# Copy common module
COPY backend/common/pom.xml backend/common/
COPY backend/common/src backend/common/src

# Copy service module
COPY backend/supplychain-service/pom.xml backend/supplychain-service/
COPY backend/supplychain-service/src backend/supplychain-service/src

# Build common first
RUN mvn -f backend/common/pom.xml install -DskipTests

# Build service
RUN mvn -f backend/supplychain-service/pom.xml package -DskipTests

# Run stage
FROM eclipse-temurin:17-jre
WORKDIR /app
COPY --from=build /app/backend/supplychain-service/target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
