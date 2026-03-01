FROM maven:3.9-eclipse-temurin-17 AS build
WORKDIR /app

# Copy root pom
COPY pom.xml .
RUN mvn -N install

# Copy common module
COPY backend/common/pom.xml backend/common/
COPY backend/common/src backend/common/src

# Copy service module
COPY backend/finance-service/pom.xml backend/finance-service/
COPY backend/finance-service/src backend/finance-service/src

# Build common first
RUN mvn -f backend/common/pom.xml install -DskipTests

# Build service
RUN mvn -f backend/finance-service/pom.xml package -DskipTests

# Run stage
FROM eclipse-temurin:17-jre
WORKDIR /app
COPY --from=build /app/backend/finance-service/target/*.jar app.jar
EXPOSE 8083
ENTRYPOINT ["java", "-jar", "app.jar"]
