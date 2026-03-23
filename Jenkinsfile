pipeline {
    agent any

    environment {
        IMAGE_NAME = 'weather-api:v1'
        AWS_REGION = "ap-south-1"
        AWS_ACCOUNT_ID = "958006149889"
        REPO_NAME = "weather-api"
        SONAR_HOST = 'http://localhost:9003'
        SONAR_PROJECT_KEY = 'weather-api'
        SCANNER_HOME = tool 'sonarqube'   
    }

    stages {

        stage('Info') {
            steps {
                echo 'Weather app CI/CD pipeline'
            }
        }

        stage('Git Checkout') {
            steps {
                git branch: 'main', credentialsId: 'git-token', url: 'https://github.com/mukilansentha-glitch/claud.git'
            }
        }

        stage('Trivy FS Scan') {
            steps {
                sh 'trivy fs --format table .'
            }
        }

        stage('SonarQube Scan') {
            steps {
                withSonarQubeEnv('sonarqube') {
                    sh """
                    ${SCANNER_HOME}/bin/sonar-scanner \
                    -Dsonar.projectName=weatherapi-app \
                    -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                    -Dsonar.sources=.
                    """
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Trivy Image Scan') {
            steps {
                sh 'trivy image --severity HIGH,CRITICAL $IMAGE_NAME'
            }
        }

        stage('Push to ECR') {
            steps {
                sh '''
                aws ecr get-login-password --region ap-south-1 | \
                docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com
        
                docker tag $IMAGE_NAME $AWS_ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/$REPO_NAME:v1
        
                docker push $AWS_ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/$REPO_NAME:v1
                '''
            }
        }

        stage('Deploy to EKS') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-cred']]) {
                    sh '''
                    aws eks update-kubeconfig --region ap-south-1 --name mukilan-eks-k8s
                    kubectl apply -f k8/deployment.yaml
                    kubectl apply -f k8/svc.yaml
                    '''
                }
            }
        }
    }

    post {
        success {
            emailext (
                subject: "SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
Job: ${env.JOB_NAME}
Build: #${env.BUILD_NUMBER}

Status: SUCCESS !!

Sonar Report:
${SONAR_HOST}/dashboard?id=${SONAR_PROJECT_KEY}

Build URL:
${env.BUILD_URL}
""",
                to: "team@example.com"
            )
        }

        failure {
            emailext (
                subject: "FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
Job: ${env.JOB_NAME}
Build: #${env.BUILD_NUMBER}

Status: FAILED!!

Sonar Report:
${SONAR_HOST}/dashboard?id=${SONAR_PROJECT_KEY}

Check details:
${env.BUILD_URL}
""",
                to: "team@example.com"
            )
        }
    }
}
