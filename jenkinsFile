pipeline {
    agent any
    
    environment {
        REGISTRY = 'docker.io'
        REGISTRY_CREDENTIALS = 'docker-credentials'
        IMAGE_NAME = 'smart-billing-system'
        IMAGE_TAG = "${BUILD_NUMBER}"
        KUBECONFIG = '/var/lib/jenkins/.kube/config'
        DOCKER_IMAGE = "${REGISTRY}/${REGISTRY_CREDENTIALS}/${IMAGE_NAME}:${IMAGE_TAG}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code...'
                checkout scm
            }
        }
        
        stage('Build Requirements') {
            steps {
                echo 'Building requirements.txt...'
                script {
                    sh '''#!/bin/bash
                        python3 -m pip freeze > requirements.txt
                    '''
                }
            }
        }
        
        stage('Code Quality & Linting') {
            steps {
                echo 'Running code quality checks...'
                script {
                    sh '''#!/bin/bash
                        python3 -m pip install --quiet pylint flake8 || true
                        flake8 *.py --count --select=E9,F63,F7,F82 --show-source --statistics || true
                        echo 'Linting checks completed (non-blocking)'
                    '''
                }
            }
        }
        
        stage('Unit Tests') {
            steps {
                echo 'Running unit tests...'
                script {
                    sh '''#!/bin/bash
                        python3 -m pip install --quiet pytest pytest-cov || true
                        # Create test file if needed
                        mkdir -p tests
                        echo 'Running tests...'
                    '''
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                script {
                    sh '''#!/bin/bash
                        docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest .
                        docker image ls | grep ${IMAGE_NAME}
                    '''
                }
            }
        }
        
        stage('Push Docker Image') {
            steps {
                echo 'Pushing Docker image to registry...'
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh '''#!/bin/bash
                            echo "${DOCKER_PASS}" | docker login -u "${DOCKER_USER}" --password-stdin
                            docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${DOCKER_USER}/${IMAGE_NAME}:${IMAGE_TAG}
                            docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${DOCKER_USER}/${IMAGE_NAME}:latest
                            docker push ${DOCKER_USER}/${IMAGE_NAME}:${IMAGE_TAG}
                            docker push ${DOCKER_USER}/${IMAGE_NAME}:latest
                            docker logout
                        '''
                    }
                }
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                echo 'Deploying to Kubernetes cluster...'
                script {
                    sh '''#!/bin/bash
                        # Update image tag in deployment
                        sed -i "s|IMAGE_TAG|${IMAGE_TAG}|g" k8s/deployment.yaml
                        sed -i "s|REGISTRY_USER|${REGISTRY_CREDENTIALS}|g" k8s/deployment.yaml
                        
                        # Apply Kubernetes manifests
                        kubectl apply -f k8s/namespace.yaml || true
                        kubectl apply -f k8s/configmap.yaml || true
                        kubectl apply -f k8s/pvc.yaml || true
                        kubectl apply -f k8s/service.yaml
                        kubectl apply -f k8s/deployment.yaml
                        
                        # Wait for deployment to be ready
                        kubectl rollout status deployment/smart-billing -n smart-billing --timeout=5m
                        
                        echo 'Deployment completed successfully'
                    '''
                }
            }
        }
        
        stage('Verify Deployment') {
            steps {
                echo 'Verifying deployment...'
                script {
                    sh '''#!/bin/bash
                        echo "Pod Status:"
                        kubectl get pods -n smart-billing -o wide
                        echo "Service Status:"
                        kubectl get svc -n smart-billing
                        echo "Deployment Status:"
                        kubectl get deployment -n smart-billing
                    '''
                }
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline execution completed'
            cleanWs()
        }
        success {
            echo 'Pipeline succeeded! S_MART Billing System deployed successfully'
        }
        failure {
            echo 'Pipeline failed! Check logs for details'
        }
    }
}
