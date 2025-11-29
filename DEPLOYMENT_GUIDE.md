# CI/CD Deployment Guide for S_MART Billing System

## Overview
This guide explains how to deploy the S_MART Tkinter Billing System using Docker, Jenkins, and Kubernetes.

## Prerequisites
- Docker and Docker Hub account
- Kubernetes cluster (v1.24+)
- Jenkins server with Kubernetes plugin
- kubectl configured
- Git repository with webhook enabled

## File Structure
```
├── Dockerfile              # Docker image configuration
├── jenkinsFile             # Jenkins pipeline definition
├── requirements.txt        # Python dependencies
├── .dockerignore          # Docker build ignore rules
├── .gitignore             # Git ignore rules
├── k8s/
│   ├── namespace.yaml     # Kubernetes namespace
│   ├── deployment.yaml    # Pod deployment configuration
│   ├── service.yaml       # Service exposure configuration
│   ├── configmap.yaml     # Application configuration
│   ├── pvc.yaml          # Persistent volume claim
│   └── serviceaccount.yaml # RBAC configuration
└── dashboard.py           # Main application entry point
```

## Deployment Steps

### 1. Docker Setup
```bash
# Build Docker image
docker build -t smart-billing-system:1.0 .

# Test image locally
docker run -it --rm smart-billing-system:1.0

# Push to Docker Hub
docker tag smart-billing-system:1.0 YOUR_DOCKER_USER/smart-billing-system:1.0
docker push YOUR_DOCKER_USER/smart-billing-system:1.0
```

### 2. Jenkins Configuration

#### Create New Pipeline Job:
1. Click "New Item" in Jenkins
2. Enter job name: "smart-billing-deploy"
3. Select "Pipeline"
4. Configure:
   - **Definition**: Pipeline script from SCM
   - **SCM**: Git
   - **Repository URL**: Your Git repo URL
   - **Branch**: */main (or your branch)
   - **Script Path**: jenkinsFile

#### Add Credentials:
1. Jenkins > Credentials > System > Global
2. Add Docker credentials:
   - Kind: Username with password
   - Username: YOUR_DOCKER_USERNAME
   - Password: YOUR_DOCKER_PASSWORD
   - ID: docker-credentials

#### Webhook Setup:
1. In your Git repository settings
2. Add webhook pointing to: `http://your-jenkins-server/github-webhook/`

### 3. Kubernetes Deployment

#### Prerequisites:
```bash
# Create namespace and resources
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/serviceaccount.yaml
```

#### Deploy Application:
```bash
# Deploy all resources
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/pvc.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Verify deployment
kubectl get pods -n smart-billing
kubectl get svc -n smart-billing
kubectl get deployment -n smart-billing

# View logs
kubectl logs -f deployment/smart-billing -n smart-billing

# Port forward for local access
kubectl port-forward svc/smart-billing-service 5900:5900 -n smart-billing
```

#### Monitor Deployment:
```bash
# Check pod status
kubectl describe pod <pod-name> -n smart-billing

# Check resource usage
kubectl top pods -n smart-billing

# Stream logs
kubectl logs -f deployment/smart-billing -n smart-billing
```

### 4. Manual Scaling
```bash
# Scale replicas
kubectl scale deployment smart-billing --replicas=3 -n smart-billing

# Check rolling update status
kubectl rollout status deployment/smart-billing -n smart-billing
```

### 5. Rolling Updates
```bash
# Update image
kubectl set image deployment/smart-billing smart-billing=YOUR_DOCKER_USER/smart-billing-system:2.0 -n smart-billing

# Rollback if needed
kubectl rollout undo deployment/smart-billing -n smart-billing
```

## Environment Variables
- `PYTHONUNBUFFERED=1` - Real-time Python output
- `DB_PATH=/data/s_mart.db` - Database location
- `ENVIRONMENT=production` - Environment mode

## Resource Limits
- **Memory Request**: 256Mi
- **Memory Limit**: 512Mi
- **CPU Request**: 250m
- **CPU Limit**: 500m

## Troubleshooting

### Pod not starting:
```bash
kubectl describe pod <pod-name> -n smart-billing
kubectl logs <pod-name> -n smart-billing
```

### Database connection issues:
```bash
# Check if PVC is mounted
kubectl exec -it <pod-name> -n smart-billing -- ls -la /data/

# Verify database
kubectl exec -it <pod-name> -n smart-billing -- sqlite3 /data/s_mart.db ".tables"
```

### Service not accessible:
```bash
kubectl get svc smart-billing-service -n smart-billing
kubectl get endpoints -n smart-billing
```

## Accessing the Application

### NodePort:
- URL: `http://<node-ip>:30900`

### Port Forward:
```bash
kubectl port-forward svc/smart-billing-service 5900:5900 -n smart-billing
# Access at: localhost:5900
```

## Cleanup
```bash
# Delete deployment
kubectl delete deployment smart-billing -n smart-billing

# Delete all resources in namespace
kubectl delete namespace smart-billing
```

## Security Notes
- Application runs as non-root user (UID 1000)
- Read-only root filesystem enabled
- SELinux capabilities restricted
- Pod Anti-affinity for high availability
- RBAC configured with minimal permissions

## Performance Tuning
- Adjust resource requests/limits based on your cluster
- Modify `replicas` field for load balancing
- Enable HPA (Horizontal Pod Autoscaler) for auto-scaling
- Configure persistent volume storage class

## Next Steps
1. Customize image tag and registry
2. Set up monitoring with Prometheus/Grafana
3. Configure ingress controller for external access
4. Implement backup strategy for databases
5. Set up log aggregation (ELK, Loki)
