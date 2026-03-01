FROM openjdk:17-jdk-slim

# Set working directory
WORKDIR /app

# Copy the JAR file
COPY target/defi-service-*.jar app.jar

# Expose port
EXPOSE 8086

# Run the application
ENTRYPOINT ["java", "-jar", "app.jar"]