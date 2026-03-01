FROM maven:3.9-eclipse-temurin-17 AS build
WORKDIR /app

# Copy root pom
COPY pom.xml .
RUN mvn -N install

# Copy common module
COPY backend/common/pom.xml backend/common/
COPY backend/common/src backend/common/src

# Copy service module
COPY backend/blockchain-service/pom.xml backend/blockchain-service/
COPY backend/blockchain-service/src backend/blockchain-service/src

# Build common first
RUN mvn -f backend/common/pom.xml install -DskipTests

# Build service
RUN mvn -f backend/blockchain-service/pom.xml package -DskipTests

# Run stage
FROM eclipse-temurin:17-jre
WORKDIR /app
COPY --from=build /app/backend/blockchain-service/target/*.jar app.jar
EXPOSE 8545
ENTRYPOINT ["java", "-jar", "app.jar"]