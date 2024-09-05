# Deploying the 2-Tier Microservices Web Application Using Docker-compose - Step-by-Step Guide

# 1. Clone the repository
     - To clone the repository run the command 
       - git clone --single-branch -b tec-2tier-microservices-deployment https://github.com/techkedgeconnect/tec-nodejs-webapp.git
     - Change into the cloned directory using this command - cd tec-nodejs-webapp
     - List the content of the cloned directory using the command - ls you will see the following file and directories
       - README
       - frontend
       - backend

# 2. Write Dockerfile for both the backend and frontend microservices
     - Writing Dockerfile for the backend microservice
       - Change directory to backend using this command - cd backend
       - list the content of the backend directory using the command - ls you will see the following files
         - app.py - file is a simple Flask application used for serving a backend API that returns a welcome message
         - requirement.txt - file lists the necessary dependencies
       - Create a Dockerfile inside the backend directory using the command and populate it with the required content 
         - sudo vi Dockerfile

     - Writing Dockerfile for the frontend microservice
       - Change directory to backend using this command - cd frontend
       - list the content of the backend directory using the command - ls you will see the following files and directory
         - app.js - creates a Node.js server with Express that serves static files, handles requests to dynamically generate HTML pages, and provides an API endpoint for               fetching data from the backend microservice.
         - package.json - defines the project's metadata, scripts for running and developing the application, dependencies for production and development, and the Node.js              version compatibility. It is essential for managing the project's lifecycle and dependencies.
         - public - the folder is crucial for storing and serving static assets that are directly accessed by users and required for the frontend microservice of the web               application
       - Create a Dockerfile inside the frontend directory using the command and populate it with the required content 
         - sudo vi Dockerfile

# 3. Add user to docker group to enable you to run docker commands
     - To add ubuntu user to docker group, run the command - sudo usermod -aG docker ubuntu && newgrp docker
     - Restart docker service by running the command - sudo systemctl restart docker
     - Confirm docker status by running the command - sudo systemctl status docker
     - Confirm you can run docker command without sudo - docker ps

# 4. Create docker images for both the backend and frontend microservices
     - Build docker image for the backend microservice 
       - Change directory to backend using this command - cd backend
       - To build the backend microservice image run the command - docker build -t backend .
       - To view the created backend microservice image, run the command - docker images

     - Build docker image for the frontend microservice 
       - Change directory to frontend using this command - cd frontend
       - To build the frontend microservice image run the command - docker build -t frontend .
       - To view the created frontend microservice image, run the command - docker images

# 5. Automate creation of Amazon Elastic Container Registry - Create a terraform module for the backend and frontend microservice repositories
     - Backend Private Repository - <aws_account_id>.dkr.ecr.<aws_region>.amazonaws.com/backend
     - Frontend Private Repository - <aws_account_id>.dkr.ecr.<aws_region>.amazonaws.com/frontend

# 6. Tag and push the images to the respective private repositories 
     - To tag and push the backend microservice image
       - Retrieve the authentication token and authenticate your Docker client to the amazon ecr registry. Use the AWS CLI: - 
         - aws ecr get-login-password --region <aws_region> | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.<aws_region>.amazonaws.com
     - Tag the image so you can push the image to this repository using the command
       - docker tag backend:latest <aws_account_id>.dkr.ecr.<aws_region>.amazonaws.com/backend:latest 
     - Push the image to the newly created backend private repository by running this command:
       - docker push <aws_account_id>.dkr.ecr.<aws_region>.amazonaws.com/backend:latest

    - To tag and push the frontend microservice image
      - Retrieve the authentication token and authenticate your Docker client to the amazon ecr registry. Use the AWS CLI: - 
        - aws ecr get-login-password --region <aws_region> | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.<aws_region>.amazonaws.com
    - Tag the image so you can push the image to this repository using the command
      - docker tag frontend:latest <aws_account_id>.dkr.ecr.<aws_region>.amazonaws.com/frontend:latest 
    - Push the image to the newly created backend private repository by running this command:
      - docker push <aws_account_id>.dkr.ecr.<aws_region>.amazon.com/frontend:latest

# 7. Build and Run the 2-Tier Microservices Application
     - Create a docker-compose.yml File
       - Navigate to the root directory of the project and create a docker-compose.yml using this command
         - sudo vi docker-compose.yml 
         - Create deployment configuration for backend and front. Also create a bridge network to enable both backend and frontend to communicate. Save the configuration
     - Build and Run the Application
       - Navigate to the root of the project directory and run the following command:
         - docker-compose up --build - This command will build and start both the backend and frontend microservices. 
           - The backend microservice will be accessible at http://localhost:5000 
           - And the frontend microservice will be accessible at http://localhost:3000.

# 8. Test the 2-Tier Microservices Application
     - Open the browser and navigate to http://localhost:3000 to see the frontend.
     - The frontend should communicate with the backend, and you should see the data from the backend displayed on the frontend.

# 9. Stop the Application
     - To stop the application, you can use this command
      - docker-compose down - This command will stop and remove the containers, networks, and volumes created by docker-compose up.

