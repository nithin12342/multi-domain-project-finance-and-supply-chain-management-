FROM node:18-alpine

WORKDIR /app

# Copy package files from the correct location based on root context
COPY frontend/web-app/package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY frontend/web-app/ .

# Build
RUN npm run build

# Expose port
EXPOSE 3000

# Start command
CMD ["npm", "start"]
