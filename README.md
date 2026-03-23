
**Weather API App - DevOps CI/CD Pipeline Project**

**Project Overview**

The Weather API App is a cloud-native application deployed on AWS using a complete DevOps CI/CD pipeline. This project demonstrates automated build, security scanning, quality checks, containerization, and deployment to Kubernetes (EKS), along with monitoring and notifications.

---

**Tools Used**

* **Version Control:** Git
* **CI/CD Tool:** Jenkins
* **Code Quality:** SonarQube
* **Security Scanning:** Trivy
* **Containerization:** Docker
* **Container Registry:** AWS ECR
* **Orchestration:** AWS EKS (Kubernetes)
* **Monitoring:** Prometheus & Grafana
* **Notifications:** Email (Jenkins configured)

---
**CI/CD Pipeline Workflow**

### 1. Code Commit

Developer pushes code to the Git repository.

### 2. Jenkins Pipeline Triggered

Pipeline automatically starts on code changes.

### 3. Code Quality Analysis

SonarQube checks:

* Code quality
* Bugs and vulnerabilities
* Code smells

### 4. Security Scan (Source Code)

Trivy scans for vulnerabilities in the codebase.

### 5. Docker Image Build

Application is containerized using Docker.

### 6. Docker Image Scan

Trivy scans the built Docker image for vulnerabilities.

### 7. Push to AWS ECR

Secure Docker image is pushed to Amazon ECR repository.

### 8. Deployment to AWS EKS

Kubernetes manifests deploy the app to the EKS cluster.
A service is created to expose the application.

### 9. Monitoring Setup

* Prometheus collects cluster and application metrics
* Grafana provides dashboards and visualization

### 10. Email Notifications

Jenkins sends notifications for:

* Build success
* Build failure

---

## Architecture Overview

Git → Jenkins → SonarQube → Trivy → Docker Build → Trivy Scan → AWS ECR → AWS EKS → Prometheus → Grafana



## Screenshots

CI CD Pipeline
<img width="1920" height="1080" alt="Successfull pipeline" src="https://github.com/user-attachments/assets/ac7c5231-a9ac-447c-a896-0fa48920ab9c" />

Sonar scanner
<img width="1920" height="1080" alt="sonanar scnner" src="https://github.com/user-attachments/assets/23af7dc5-87b2-49f4-9a01-884231261354" />

EKS server
<img width="1920" height="1080" alt="EKS cluster" src="https://github.com/user-attachments/assets/d070e247-235e-47cd-aecd-4d16b7e3ffc1" />

EC2 instences
<img width="1920" height="1080" alt="instences" src="https://github.com/user-attachments/assets/a699ba05-1ba3-494f-bf6e-629b886e56ee" />

ECR Repo
<img width="1920" height="1080" alt="ECR Repo" src="https://github.com/user-attachments/assets/94f07c7f-3c13-40a1-9fcd-35b9c056e5e6" />
<img width="1920" height="1080" alt="Image in repo" src="https://github.com/user-attachments/assets/87e6c438-ff28-4948-90bc-d0159d6239a5" />

K8s details
<img width="1920" height="1080" alt="k8s details" src="https://github.com/user-attachments/assets/626c9573-8b38-474c-83db-5e1bbdeb5a9e" />

Mail notification
<img width="1920" height="1080" alt="mail notification" src="https://github.com/user-attachments/assets/fe20ba0a-7966-44bc-b01d-cfe3310aede1" />

Promethius & Grafana 
<img width="1920" height="1080" alt="prometheus" src="https://github.com/user-attachments/assets/3e6f0f81-a561-4665-b67f-f3789b5fcdd3" />
<img width="1920" height="1080" alt="grafana dashboard" src="https://github.com/user-attachments/assets/de4a672f-f53d-4675-a81a-89e34127cae4" />
<img width="1920" height="1080" alt="Screenshot 2026-03-23 150742" src="https://github.com/user-attachments/assets/ff666eee-f71d-49e0-8846-a9cae5083aad" />
<img width="1920" height="1080" alt="Screenshot 2026-03-23 150701" src="https://github.com/user-attachments/assets/e1adccc0-8b3c-4d66-a040-5422341932a3" />

Weather app results

<img width="1920" height="1080" alt="weather app working" src="https://github.com/user-attachments/assets/cda3f852-b39b-4b01-9fac-17ac66372f55" />
<img width="1920" height="1080" alt="weather app dashboard" src="https://github.com/user-attachments/assets/b008b667-7ac2-46bf-b0a6-9c8befa6ee97" />
