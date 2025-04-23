FROM node:20

WORKDIR /app

# Install Wasp CLI
RUN curl -sSL https://get.wasp-lang.dev/installer.sh | sh

# Add wasp to PATH
ENV PATH="/root/.local/bin:${PATH}"

# Copy package.json and package-lock.json first for better layer caching
COPY ./app/package*.json ./

# Skip separate dependency installation since they're now in package.json

# Install dependencies required for Wasp
RUN npm ci

# Copy the rest of the application code
COPY ./app ./

# Update the API URL in the ShowBuddy client to use the backend service
RUN sed -i 's|http://localhost:8000|http://showbuddy-python:8000|g' ./src/showbuddy/showbuddy.ts

# Expose the port
EXPOSE 3000

# Start the app in development mode with hot reloading
CMD ["wasp", "start"]