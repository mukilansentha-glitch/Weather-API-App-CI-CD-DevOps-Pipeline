pipeline {
    agent any

    environment {
        SONAR_TOKEN        = credentials('sonar-token')
        SONAR_HOST         = 'http://localhost:9000'          // ← change to your SonarQube URL
        OPENWEATHER_API_KEY = credentials('openweather-api-key')
        IMAGE_NAME         = 'world-weather-app'
        APP_PORT           = '5000'
        VENV               = '.venv'
        PY                 = '.venv/bin/python'
        PIP                = '.venv/bin/pip'
        PYTEST             = '.venv/bin/pytest'
        FLAKE8             = '.venv/bin/flake8'
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
        timeout(time: 30, unit: 'MINUTES')
    }

    stages {

        // ── 1. Checkout ──────────────────────────────────
        stage('Checkout') {
            steps {
                checkout scm
                sh 'echo "Commit: ${GIT_COMMIT} | Branch: ${GIT_BRANCH}"'
            }
        }

        // ── 2. Install dependencies ──────────────────────
        stage('Install') {
            steps {
                sh '''
                    python3 -m venv ${VENV}
                    ${PIP} install --upgrade pip
                    ${PIP} install -r requirements.txt
                '''
            }
        }

        // ── 3. Lint ──────────────────────────────────────
        stage('Lint') {
            steps {
                sh '${FLAKE8} app/ tests/'
            }
            post {
                failure { echo 'Lint failed — fix flake8 errors.' }
            }
        }

        // ── 4. Tests + Coverage ──────────────────────────
        stage('Test & Coverage') {
            steps {
                sh '${PYTEST} --junitxml=test-results.xml'
            }
            post {
                always {
                    junit 'test-results.xml'
                    publishHTML(target: [
                        reportDir:   'htmlcov',
                        reportFiles: 'index.html',
                        reportName:  'Coverage Report',
                        keepAll:     true,
                        alwaysLinkToLastBuild: true,
                        allowMissing: false
                    ])
                }
                failure { echo 'Tests failed or coverage below 80%.' }
            }
        }

        // ── 5. SonarQube Analysis ────────────────────────
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh '''
                        sonar-scanner \
                          -Dsonar.projectKey=Weather-app \
                          -Dsonar.projectName=Weather-app \
                          -Dsonar.sources=. \
                          -Dsonar.language=py \
                          -Dsonar.python.coverage.reportPaths=coverage.xml \
                          -Dsonar.exclusions="**/static/**,**/templates/**,**/__pycache__/**,**/htmlcov/**,**/.venv/**" \
                          -Dsonar.test.inclusions="tests/**,**/test_*.py" \
                          -Dsonar.host.url=${SONAR_HOST} \
                          -Dsonar.token=${SONAR_TOKEN}
                    '''
                }
            }
        }

        // ── 6. Quality Gate ──────────────────────────────
        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
            post {
                failure { echo 'SonarQube Quality Gate FAILED — pipeline aborted.' }
                success { echo 'Quality Gate PASSED.' }
            }
        }

        // ── 7. Docker Build ──────────────────────────────
        stage('Docker Build') {
            steps {
                sh '''
                    docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .
                    docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest
                    echo "Image built: ${IMAGE_NAME}:${BUILD_NUMBER}"
                '''
            }
        }

        // ── 8. Deploy ────────────────────────────────────
        stage('Deploy') {
            steps {
                sh '''
                    docker stop ${IMAGE_NAME} || true
                    docker rm   ${IMAGE_NAME} || true
                    docker run -d \
                      --name ${IMAGE_NAME} \
                      -p ${APP_PORT}:5000 \
                      -e OPENWEATHER_API_KEY=${OPENWEATHER_API_KEY} \
                      --restart unless-stopped \
                      ${IMAGE_NAME}:latest
                    echo "Deployed at http://localhost:${APP_PORT}"
                '''
            }
        }
    }

    post {
        always   { cleanWs() }
        success  { echo "SUCCESS — Build #${BUILD_NUMBER}" }
        failure  { echo "FAILED  — Build #${BUILD_NUMBER}" }
    }
}
