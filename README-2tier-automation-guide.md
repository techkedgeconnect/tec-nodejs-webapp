# Set up a GitOps Workflow using GitHub Actions to Automate the Deployment of the 2-tier Microservices Web aAplication
  Leveraging GitHub Secrets for storing credentials, AWS ECR for image storage, Helm for packaging, ArgoCD for managing Kubernetes resources, 
  and Kubernetes for hosting the application.

# Key Components of the GitOps Action CICD Workflow
  - GitHub Actions - Automates the CI pipeline
  - GitHub Secrets - Securely stores credentials (AWS, ECR, ArgoCD)
  - AWS ECR - Stores the Docker images for the backend and frontend services
  - Helm - Manages Kubernetes deployments as charts
  - ArgoCD - Syncs and manages application deployments in the Kubernetes cluster
  - NGINX - Optionally used for load balancing traffic to the app

# Step-by-Step GitOps Action CI Pipeline Workflow
This pipeline will build the Docker images for both frontend and backend, push them to Amazon ECR, 
update the image tag in the values.yaml file, and commit the changes back to the GitHub repository.
1. Set Up GitHub Secrets
   Before writing the GitHub Actions workflow, you need to store the following secrets in your GitHub repository under
   Settings > Secrets and variables > Actions > New repository secret:
   -AWS_ACCESS_KEY_ID — AWS Access Key ID
   - AWS_SECRET_ACCESS_KEY — AWS Secret Access Key
   - AWS_REGION — The region of your ECR repository (e.g., eu-west-2)
   - ECR_REGISTRY — Your ECR registry URL (e.g., <aws_account_id>.dkr.ecr.<aws_region>.amazonaws.com)
   - ARGOCD_AUTH_TOKEN — ArgoCD authentication token for API access
   - ARGOCD_SERVER_URL — ArgoCD server URL (e.g., https://argocd.example.com)
  
2. Install and Cconfigure Helm - If Helm is not installed, you can install it using the following commands
   - curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
   - Verify Helm installation by executing this command - helm version
   - Create a Helm Chart for the 2-tier microservices application by creating /helm directory and change into it
     - mkdir /helm && cd /helm
     - helm create tec-web-app - This command creates a new directory tec-web-app/ with a pre-configured chart structure
   - Modify the Helm Chart for Your Application - Edit the values.yaml file inside the tec-web-app directory.
     This file holds the configuration for your chart.
   - Define Frontend and Backend Deployments - Create your deployment manifests inside the templates directory
     for both frontend and backend deployments
   - Define Services - Create the services for both frontend and backend inside the templates directory

3. Create a namespace for your application deployment by executing this command
   - kubectl create namespace tec-web-app
     
4. Create a .github/workflows/CI-2tier-deployment.yml (CI Workflow) comprising the following stages;
   - Trigger - The CI pipeline is triggered on every push to the project branch
   - Set up Docker Buildx - Both backend and frontend Docker images are built and tagged with the ECR registry URL, which is stored as a GitHub Secret.
   - Fetch AWS Credentials from Secrets - The AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, and ECR_REGISTRY
     are fetched from GitHub Secrets using ${{ secrets.<SECRET_NAME> }}
   - Log in to ECR - Use AWS credentials from GitHub Secrets to log in to ECR, allowing Docker to push images to the ECR repository
   - Build and Push Docker Images - The backend and frontend Docker images are built and tagged with the GitHub run ID (${{ github.run_id }}).
     The images are then pushed to Amazon ECR
   - Update values.yaml - The values.yaml file inside the Helm chart is updated with the new image tags (${{ github.run_id }})
   - Commit Changes - The updated values.yaml file is committed back to the GitHub repository,
     which will trigger the CD pipeline or deployment of the application using ARGOCD

# Note
  - Helm Chart Structure - The Helm chart is located in /helm/tec-web-app and contains all the necessary manifests
    for deploying the backend and frontend services
  - Helm Chart Update with github.run_id - After building and pushing the Docker images, the workflow updates the Helm chart values by passing the new 
    backendTag and frontendTag parameters to Helm using the --set flag.
    - This ensures that the new version of the application (based on the new image tags) is deployed. Example Helm chart variables
      image:
       repository: <aws_account_id>.dkr.ecr.<aws_region>.amazonaws.com
       backendTag: "{{ .Values.image.backendTag }}"
       frontendTag: "{{ .Values.image.frontendTag }}"
  - Using the github.run_id for Docker Image Tags - Instead of using the latest tag, the images are tagged with ${{ github.run_id }},
    which is a unique ID for each GitHub Actions run.
    - This ensures that each build creates a new version of the Docker image with a unique tag. For example, if the github.run_id is 12345678, the 
      backend image will be pushed as: <aws_account_id>.dkr.ecr.<aws_region>.amazonaws.com/backend-service:12345678

5. Implement Continuous Delivery Using ARGOCD
   - ArgoCD is a declarative, GitOps-based continuous delivery tool for Kubernetes.
     It enables automated deployment, monitoring, and management of Kubernetes applications by continuously
     syncing the desired state from a Git repository to the Kubernetes cluster.
   - Install ArgoCD on your Kubernetes cluster using manifests
     - kubectl create namespace argocd
     - kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
   - To access the Argo CD UI (Loadbalancer service)
     - Execute this command kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'
   - To get the Loadbalancer service IP
     - Execute this command kubectl get svc argocd-server -n argocd - to get the argocd external address/ip and paste in the browser to access it
       or you can as well get the argocd external IP address by running the command
       - kubectl get nodes -o wide - copy the external ip address, paste in the browser, add the port number in order to access the argocd UI
    - Provide the username - admin
      - For the password you need to run this command - kubectl get secret -n argocd - as part of the output you will find argocd-initial-admin-Secret 
      - To extract the argocd secret run the command - kubectl edit secret argocd-initial-admin-secret -n argocd - extract the base64 encoded password 
      - To decode the password use this command - echo <base64 encoded password> | base64 --decode
      - Use the decoded password on argocd UI to sign-in - note argocd is on the same kubernetes cluster

   - Configure ArgoCD Application to point to the GitHub repository where your Helm chart resides through ArgoCD UI or CLI
     - Application Name: tec-web-app
     - Project: Default
     - Repository URL: Your GitHub repo
     - Path: /helm/tec-web-app
     - Namespace: tec-web-app
     - Sync Policy: Set to Automatic to automatically apply changes.

   - Using CLI by executing this command
   - argocd app create tec-web-app \ --repo https://github.com/<your-github-repo>.git \ --path /helm/tec-web-app \
     --dest-server https://kubernetes.default.svc \ --dest-namespace tec-web-app \ --sync-policy automated

This configuration ensures that whenever there are new commits to the Helm chart or image tags, ArgoCD will automatically pull and deploy the updates.

6. Deployment Phase (Deploy using ArgoCD)
   - The application deployment is triggered whenever there is a change to the values.yaml file
   (which happens when the CI pipeline pushes the changes). This will automatically sync the ArgoCD application,
   ensuring that the Kubernetes cluster uses the newly tagged images.

7. Verify end-to-end CICD by making changes in our code
   - Try modify the content of index.html file in the frontend public directory - Enhance your Cloud and DevOps skills to accelerate your earning
      potential
   - Commit the changes
   - The commit should automatically trigger the CI - build docker image with new git runner ID tag and push to Amazon ECR private repo for both the
     backend and frontend services with - the image tags updated in the helm chart values.yaml file
     - Confirm the new tag created in the Amazon ECR private repository is the same as the updated image tags in helm chart values.yaml file
   - ArgoCD should pick up the new change and deploy the application latest version - ArgoCD by default look for the new changes
   - To confirm the new changes run the command
     - kubectl edit deploy - you will notice that the application image has chnaged from the previous version to the newly created image version
   - Verify the changes by browsing the application URL

With this we have been able to automate the 2tier microservices application deployment by implementing an end to end CICD workflow using Github action for the CI and ArgoCD for the CD

# Note
  The deployment is done to an existing Amazon Elastic Kubernetes Service 3-node cluster
