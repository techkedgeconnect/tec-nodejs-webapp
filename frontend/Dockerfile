FROM node:18-slim

# Add a label to the Docker image
LABEL email="techkedgeconnect@gmail.com"

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the package.json and package-lock.json (if available)
COPY package*.json ./

# Install the dependencies (only production dependencies are installed)
RUN npm install

# Copy the rest of the application code into the container
COPY . .

# Expose port 3000 to the outside world
EXPOSE 3000

# Command to run the frontend application
CMD ["node", "app.js"]
