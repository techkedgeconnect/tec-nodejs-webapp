# Helm-ArgoCD Project for 2-Tier Microservices Deployment

## Overview

This project demonstrates the use of Helm charts and ArgoCD to automate the deployment of a 2-tier microservices application comprising a frontend written in Nodejs and a backend developed using Python (Flask). The project is designed to automatically deploy updates to the microservices whenever changes are pushed to the Helm charts in the Source Code Management (SCM) repository. The deployment takes place in a self-managed Kubernetes cluster on AWS.

## Project Structure

The repository is organized as follows:

- **`K8s/`**: Contains Kubernetes manifests for deploying the backend and frontend services.
  - `backend-deployment.yaml`: Kubernetes deployment manifest for the backend service.
  - `backend-svc.yaml`: Kubernetes service manifest for the backend service.
  - `frontend-deployment.yaml`: Kubernetes deployment manifest for the frontend service.
  - `frontend-svc.yaml`: Kubernetes service manifest for the frontend service.
    
  - **`backend/`**: Contains the backend microservice code and Docker configuration.
  - `Dockerfile`: Dockerfile to build the backend service image.
  - `app.py`: Backend application code.
  - `requirements.txt`: Python dependencies for the backend service.

- **`frontend/`**: Contains the frontend microservice code and Docker configuration.
  - `Dockerfile`: Dockerfile to build the frontend service image.
  - `app.js`: Frontend application code.
  - `package.json`: Node.js dependencies for the frontend service.

- **`helm-charts/`**: Contains Helm charts for the microservices.
  - `backend/`: Helm chart for the backend service.
    - `templates/`: Contains Kubernetes templates for deployment and service.
    - `values.yaml`: Default values for the backend Helm chart.
  - `frontend/`: Helm chart for the frontend service.
    - `templates/`: Contains Kubernetes templates for deployment and service.
    - `values.yaml`: Default values for the frontend Helm chart.

- **`terraform/`**: (Optional) Terraform scripts for infrastructure provisioning (if applicable).
  - `main.tf`: Terraform configuration file.

## Prerequisites

To run this project, you will need the following:

- **Amazon Web Services (AWS) Account**: For deploying the application to GKE.
- **Self-Managed Cluster**: A Kubernetes cluster in AWS.
- **Helm**: To package and manage Kubernetes applications using Helm charts.
- **ArgoCD**: A GitOps continuous delivery tool for Kubernetes.
- **Docker**: For containerizing the microservices.
- **Git**: For version control and pushing changes to the SCM repository.

## Setup Instructions

### 1. Clone the Repository

Clone this repository to your local machine:

git clone https://github.com/techkedgeconnect/tec-nodejs-webapp.git
cd tec-nodejs-webapp

### 2. Build and Push Docker Images

# Backend
cd backend
docker build -t gcr.io/your-project-id/backend:latest .
docker push gcr.io/your-project-id/backend:latest

# Frontend
cd ../frontend
docker build -t gcr.io/your-project-id/frontend:latest .
docker push gcr.io/your-project-id/frontend:latest

### 3. Deploy with Helm
# Deploy backend
helm install backend helm-charts/backend --namespace your-namespace

# Deploy frontend
helm install frontend helm-charts/frontend --namespace your-namespace

### 4. Set Up ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

### 5. Create an ArgoCD application that points to your Helm chart in the GitHub repository.

### 6. Set up automated sync to trigger deployments on SCM changes.

### 7. Test the Deployment
Change your Helm charts and push them to the SCM repository. ArgoCD should automatically detect the change and deploy the updated microservices to the GKE cluster.
