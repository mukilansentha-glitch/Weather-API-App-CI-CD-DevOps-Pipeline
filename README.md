**Weather API App - DevOps CI/CD Pipeline Project**

**Project Overview**
  The Weather API App is a cloud-native application deployed on AWS using a complete DevOps CI/CD pipeline. This project demonstrates automated build, security scanning, quality checks, containerization, and deployment to Kubernetes (EKS), along with monitoring and notifications.

**Tooles used **
Version Control:     Git
CI/CD Tool:          Jenkins
Code Quality:        SonarQube
Security Scanning:   Trivy
Containerization:    Docker
Container Registry:  AWS ECR
Orchestration:       AWS EKS (Kubernetes)
Monitoring:          Prometheus & Grafana
Notifications:       Email (Jenkins configured)

**CI/CD Pipeline Workflow**
Code Commit
Developer pushes code to Git repository.
Jenkins Pipeline Triggered
Pipeline automatically starts on code changes.
Code Quality Analysis
SonarQube checks:
Code quality
Bugs & vulnerabilities
Code smells
Security Scan (Source Code)
Trivy scans for vulnerabilities in the codebase.
Docker Image Build
Application is containerized using Docker.
Docker Image Scan
Trivy scans the built Docker image for vulnerabilities.
Push to AWS ECR
Secure Docker image is pushed to Amazon ECR repository.
Deployment to AWS EKS
Kubernetes manifests deploy the app to EKS cluster.
Service is created to expose the application.
Monitoring Setup
Prometheus collects cluster and app metrics.
Grafana provides dashboards and visualization.
Email Notifications
Jenkins sends notifications for:
Build success 
Build failure

Architecture Overview

Git → Jenkins → SonarQube → Trivy → Docker Build → Trivy Scan → AWS ECR → AWS EKS → Prometheus → Grafana
