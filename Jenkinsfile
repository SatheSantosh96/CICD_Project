pipeline {
    agent {
        kubernetes {
            yaml '''
apiVersion: v1
kind: Pod
spec:
  containers:

  - name: python
    image: python:3.10
    command: ['cat']
    tty: true

  - name: sonar-scanner
    image: sonarsource/sonar-scanner-cli
    command: ['cat']
    tty: true

  - name: kubectl
    image: bitnami/kubectl:latest
    command: ['cat']
    tty: true
    securityContext:
      runAsUser: 0
    env:
    - name: KUBECONFIG
      value: /kube/config
    volumeMounts:
    - name: kubeconfig-secret
      mountPath: /kube/config
      subPath: kubeconfig

  - name: dind
    image: docker:dind
    args: ["--storage-driver=overlay2"]
    securityContext:
      privileged: true
    env:
    - name: DOCKER_TLS_CERTDIR
      value: ""

  volumes:
  - name: kubeconfig-secret
    secret:
      secretName: kubeconfig-secret
'''
        }
    }

    environment {
        IMAGE_NAME = "smart-billing-system"
        IMAGE_TAG = "${BUILD_NUMBER}"
        REGISTRY_URL = "docker.io"
    }

    stages {

        stage('Checkout Code') {
            steps {
                echo "Pulling project from GitHub..."
                checkout scm
            }
        }

        stage('Install Requirements') {
            steps {
                container('python') {
                    sh '''
                      python3 -m pip install --upgrade pip
                      pip install -r requirements.txt || true
                    '''
                }
            }
        }

        stage('Static Code Quality (flake8)') {
            steps {
                container('python') {
                    sh '''
                      pip install flake8 || true
                      flake8 . || true
                    '''
                }
            }
        }

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

        stage('Build Docker Image') {
            steps {
                container('dind') {
                    withCredentials([usernamePassword(credentialsId: 'docker-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh '''
                          echo "Waiting for Docker daemon..."
                          sleep 15
                          
                          echo "Logging into Docker Hub..."
                          echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin

                          echo "Building Docker image..."
                          docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .

                          docker tag ${IMAGE_NAME}:${IMAGE_TAG} $DOCKER_USER/${IMAGE_NAME}:${IMAGE_TAG}
                          docker tag ${IMAGE_NAME}:${IMAGE_TAG} $DOCKER_USER/${IMAGE_NAME}:latest
                        '''
                    }
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                container('dind') {
                    withCredentials([usernamePassword(credentialsId: 'docker-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh '''
                          echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                          docker push $DOCKER_USER/${IMAGE_NAME}:${IMAGE_TAG}
                          docker push $DOCKER_USER/${IMAGE_NAME}:latest
                        '''
                    }
                }
            }
        }

        stage('Create Namespace') {
            steps {
                container('kubectl') {
                    sh '''
                      kubectl get namespace smart-billing || kubectl create namespace smart-billing
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                container('kubectl') {
                    sh '''
                      sed -i "s|IMAGE_TAG|${IMAGE_TAG}|g" k8s/deployment.yaml
                      sed -i "s|DOCKER_USER|${DOCKER_USER}|g" k8s/deployment.yaml

                      kubectl apply -f k8s/service.yaml -n smart-billing
                      kubectl apply -f k8s/deployment.yaml -n smart-billing

                      kubectl rollout status deployment/smart-billing -n smart-billing --timeout=5m
                    '''
                }
            }
        }

        stage('Debug ImagePullBackOff') {
            steps {
                container('kubectl') {
                    sh '''
                      kubectl describe pod -l app=smart-billing -n smart-billing || true
                      kubectl get events -n smart-billing --sort-by=.lastTimestamp | tail -n 20 || true
                    '''
                }
            }
        }

        stage('Show Cluster Status') {
            steps {
                container('kubectl') {
                    sh '''
                      kubectl get nodes -o wide
                      kubectl get svc -n smart-billing
                      kubectl get pods -n smart-billing -o wide
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "🚀
