#!/bin/bash

# S_MART Billing System - Quick Deployment Script
# This script automates the Kubernetes deployment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
DOCKER_USER="${DOCKER_USER:-your-docker-username}"
IMAGE_NAME="smart-billing-system"
NAMESPACE="smart-billing"
RELEASE_VERSION="${1:-latest}"

echo -e "${YELLOW}=== S_MART Billing System Deployment ===${NC}"

# Function to print colored output
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    print_info "Checking prerequisites..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed"
        exit 1
    fi
    
    if ! command -v kubectl &> /dev/null; then
        print_error "kubectl is not installed"
        exit 1
    fi
    
    print_info "Prerequisites OK"
}

# Build Docker image
build_image() {
    print_info "Building Docker image: ${IMAGE_NAME}:${RELEASE_VERSION}"
    docker build -t ${IMAGE_NAME}:${RELEASE_VERSION} -t ${IMAGE_NAME}:latest .
    print_info "Image built successfully"
}

# Push Docker image
push_image() {
    print_info "Pushing image to Docker Hub..."
    
    if [ "$DOCKER_USER" = "your-docker-username" ]; then
        print_error "Please set DOCKER_USER environment variable"
        exit 1
    fi
    
    docker tag ${IMAGE_NAME}:${RELEASE_VERSION} ${DOCKER_USER}/${IMAGE_NAME}:${RELEASE_VERSION}
    docker tag ${IMAGE_NAME}:${RELEASE_VERSION} ${DOCKER_USER}/${IMAGE_NAME}:latest
    docker push ${DOCKER_USER}/${IMAGE_NAME}:${RELEASE_VERSION}
    docker push ${DOCKER_USER}/${IMAGE_NAME}:latest
    print_info "Image pushed successfully"
}

# Deploy to Kubernetes
deploy_kubernetes() {
    print_info "Deploying to Kubernetes namespace: ${NAMESPACE}"
    
    # Create namespace
    kubectl create namespace ${NAMESPACE} --dry-run=client -o yaml | kubectl apply -f -
    
    # Apply manifests
    print_info "Applying namespace..."
    kubectl apply -f k8s/namespace.yaml
    
    print_info "Applying RBAC..."
    kubectl apply -f k8s/serviceaccount.yaml
    
    print_info "Applying ConfigMap..."
    kubectl apply -f k8s/configmap.yaml
    
    print_info "Applying PVC..."
    kubectl apply -f k8s/pvc.yaml
    
    print_info "Updating deployment image..."
    # Update image in deployment
    sed -i "s|REGISTRY_USER|${DOCKER_USER}|g" k8s/deployment.yaml
    sed -i "s|IMAGE_TAG|${RELEASE_VERSION}|g" k8s/deployment.yaml
    
    print_info "Applying deployment..."
    kubectl apply -f k8s/deployment.yaml
    
    print_info "Applying service..."
    kubectl apply -f k8s/service.yaml
    
    print_info "Waiting for deployment to be ready (timeout: 5 minutes)..."
    kubectl rollout status deployment/smart-billing -n ${NAMESPACE} --timeout=5m
    
    print_info "Deployment completed successfully"
}

# Verify deployment
verify_deployment() {
    print_info "Verifying deployment..."
    
    echo ""
    print_info "Pod Status:"
    kubectl get pods -n ${NAMESPACE} -o wide
    
    echo ""
    print_info "Service Status:"
    kubectl get svc -n ${NAMESPACE}
    
    echo ""
    print_info "Deployment Status:"
    kubectl get deployment -n ${NAMESPACE}
    
    echo ""
    print_info "Accessing the application:"
    echo "  NodePort: http://<NODE_IP>:30900"
    echo "  Port Forward: kubectl port-forward svc/smart-billing-service 5900:5900 -n ${NAMESPACE}"
}

# Cleanup
cleanup() {
    print_warning "Deleting deployment..."
    kubectl delete namespace ${NAMESPACE} || true
    print_info "Cleanup completed"
}

# Main menu
show_menu() {
    echo ""
    echo "Select an option:"
    echo "1) Check prerequisites"
    echo "2) Build Docker image"
    echo "3) Push Docker image"
    echo "4) Deploy to Kubernetes"
    echo "5) Verify deployment"
    echo "6) Full deployment (all steps)"
    echo "7) Cleanup"
    echo "8) Exit"
    echo ""
}

# Main script
if [ $# -eq 0 ]; then
    # Interactive mode
    while true; do
        show_menu
        read -p "Enter your choice [1-8]: " choice
        
        case $choice in
            1) check_prerequisites ;;
            2) build_image ;;
            3) push_image ;;
            4) deploy_kubernetes ;;
            5) verify_deployment ;;
            6)
                check_prerequisites
                build_image
                push_image
                deploy_kubernetes
                verify_deployment
                ;;
            7) cleanup ;;
            8) 
                print_info "Exiting..."
                exit 0
                ;;
            *)
                print_error "Invalid option. Please try again."
                ;;
        esac
    done
else
    # Command line mode
    case $1 in
        check) check_prerequisites ;;
        build) build_image ;;
        push) push_image ;;
        deploy) deploy_kubernetes ;;
        verify) verify_deployment ;;
        full)
            check_prerequisites
            build_image
            push_image
            deploy_kubernetes
            verify_deployment
            ;;
        cleanup) cleanup ;;
        *)
            echo "Usage: $0 {check|build|push|deploy|verify|full|cleanup} [version]"
            exit 1
            ;;
    esac
fi
