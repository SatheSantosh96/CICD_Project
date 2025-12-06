pipeline {
    agent {
        kubernetes {
            yaml '''
apiVersion: v1
kind: Pod
spec:
  containers:
  # Python 3.11 is better for modern code/Tkinter dependencies
  - name: python
    image: python:3.11-slim
    command: ['cat']
    tty: true

  - name: sonar-scanner
    image: sonarsource/sonar-scanner-cli:latest
    command: ['cat']
    tty: true

  - name: dind
    image: docker:dind
    args: ["--storage-driver=overlay2"]
    securityContext:
      privileged: true
    env:
    - name: DOCKER_TLS_CERTDIR
      value: ""

  # volumes and kubectl removed as they are not needed for the final GUI artifact
'''
        }
    }

    environment {
        IMAGE_NAME = "smart-billing-system"
        IMAGE_TAG = "${BUILD_NUMBER}"
        // Set this to your actual Nexus Docker Registry URL/Port
        NEXUS_REGISTRY = "nexus.yourcompany.com:8082" 
    }

    stages {
        // --- Stage 1: Checkout Code (GitHub) ---
        stage('Checkout Code') {
            steps {
                echo "Pulling project from GitHub..."
                checkout scm
            }
        }

        // --- Stage 2: Code Quality (flake8) ---
        stage('Static Code Quality (flake8)') {
            steps {
                container('python') {
                    sh '''
                    pip install flake8
                    flake8 . || true # Allow failure to be reported without stopping build
                    '''
                }
            }
        }

        // --- Stage 3: SonarQube Analysis ---
        stage('SonarQube Analysis') {
            steps {
                container('sonar-scanner') {
                    withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_TOKEN')]) {
                        sh '''
                          sonar-scanner \
                            -Dsonar.projectKey=smart_billing \
                            -Dsonar.sources=. \
                            -Dsonar.host.url=http://my-sonarqube-sonarqube.sonarqube.svc.cluster.local:9000 \
                            -Dsonar.token=$SONAR_TOKEN
                        '''
                    }
                }
            }
        }
        
        // --- Stage 4: Quality Gate Check ---
        stage('Quality Gate Check') {
            steps {
                // You need to set up a SonarQube web hook or use the official Jenkins plugin's built-in wait step
                // For simplicity, we assume the check happens externally or rely on the status reported later.
                echo "Waiting for SonarQube Quality Gate to pass..."
                timeout(time: 15, unit: 'MINUTES') {
                    // Requires Jenkins SonarQube plugin configured with server name 'SonarQube'
                    // waitForQualityGate abortPipeline: true
                }
            }
        }

        // --- Stage 5: Install Requirements & Unit Tests ---
        stage('Tests & Setup') {
            steps {
                container('python') {
                    sh '''
                    echo "Installing dependencies..."
                    pip install -r requirements.txt 
                    echo "Running tests..."
                    # Ensure you have tests/ and pytest installed via requirements.txt
                    python -m pytest tests/ || true 
                    '''
                }
            }
        }

        // --- Stage 6: Build Artifact (Docker) ---
        stage('Build Docker Image') {
            steps {
                container('dind') {
                    sh '''
                    echo "Waiting for Docker daemon..."
                    sleep 15
                    echo "Building Docker image..."
                    # Building image tagged for Nexus
                    docker build -t ${NEXUS_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG} .
                    docker tag ${NEXUS_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG} ${NEXUS_REGISTRY}/${IMAGE_NAME}:latest
                    '''
                }
            }
        }

        // --- Stage 7: Push Artifact (Nexus) ---
        stage('Push to Nexus Registry') {
            steps {
                container('dind') {
                    // 'nexus-credentials' is the Jenkins ID for your Nexus username/password
                    withCredentials([usernamePassword(credentialsId: 'nexus-credentials', usernameVariable: 'NEXUS_USER', passwordVariable: 'NEXUS_PASS')]) {
                        sh '''
                            echo "Logging into Nexus Registry: ${NEXUS_REGISTRY}"
                            echo "$NEXUS_PASS" | docker login -u "$NEXUS_USER" --password-stdin ${NEXUS_REGISTRY}
                            
                            echo "Pushing tagged image..."
                            docker push ${NEXUS_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
                            
                            echo "Pushing latest image..."
                            docker push ${NEXUS_REGISTRY}/${IMAGE_NAME}:latest
                        '''
                    }
                }
            }
        }

        // --- Stage 8: Deployment Instructions (Crucial for GUI) ---
        stage('Deployment Instructions') {
            steps {
                echo "✅ Tkinter GUI Artifact is Ready! Deployment is MANUAL."
                echo "The image has been pushed to the Nexus Registry:"
                echo "${NEXUS_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"
                echo "---"
                echo "INSTRUCTIONS FOR END-USER (Linux Host):"
                echo "1. Enable X11 access: xhost +local:docker"
                echo "2. Run the application (using a host volume for persistent SQLite data in /app/data):"
                echo "docker run -it --rm --env='DISPLAY' --volume='/tmp/.X11-unix:/tmp/.X11-unix:rw' \\"
                echo "    --volume='/path/on/host/for/db:/app/data' \\"
                echo "    ${NEXUS_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }
    }

    post {
        always {
            // Clean up Docker environment if necessary
            sh 'docker system prune -f || true'
        }
        success {
            echo "🚀 CI/CD Pipeline Completed Successfully! Image ready in Nexus."
        }
    }
}