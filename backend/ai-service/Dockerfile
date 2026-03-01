FROM maven:3.9-eclipse-temurin-17 AS build
WORKDIR /app

# Copy root pom
COPY pom.xml .
RUN mvn -N install

# Copy common module
COPY backend/common/pom.xml backend/common/
COPY backend/common/src backend/common/src

# Copy service module
COPY backend/ai-service/pom.xml backend/ai-service/
COPY backend/ai-service/src backend/ai-service/src
COPY backend/ai-service/src/main/resources backend/ai-service/src/main/resources

# Build common first
RUN mvn -f backend/common/pom.xml install -DskipTests

# Build service
RUN mvn -f backend/ai-service/pom.xml package -DskipTests

# Run stage
FROM eclipse-temurin:17-jre
WORKDIR /app
COPY --from=build /app/backend/ai-service/target/*.jar app.jar

# Install Python for AI service
RUN apt-get update && apt-get install -y python3 python3-pip

EXPOSE 8082
ENTRYPOINT ["java", "-jar", "app.jar"]