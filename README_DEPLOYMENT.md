# S_MART Billing System - CI/CD Deployment

Complete CI/CD pipeline setup for deploying the S_MART Tkinter Billing System using Docker, Jenkins, and Kubernetes.

## 📁 Deployment Files

### Docker Configuration
- **`Dockerfile`** - Multi-stage Docker image configuration
- **`.dockerignore`** - Docker build ignore rules
- **`requirements.txt`** - Python dependencies

### Jenkins CI/CD Pipeline
- **`jenkinsFile`** - Jenkins declarative pipeline with 8 stages
- **`JENKINS_SETUP.md`** - Complete Jenkins configuration guide

### Kubernetes Manifests (in `k8s/`)
- **`namespace.yaml`** - Kubernetes namespace creation
- **`deployment.yaml`** - Pod deployment with 2 replicas
- **`service.yaml`** - NodePort and Headless services
- **`configmap.yaml`** - Application configuration
- **`pvc.yaml`** - Persistent volume for database
- **`serviceaccount.yaml`** - RBAC configuration

### Deployment Scripts
- **`deploy.sh`** - Bash deployment automation script (Linux/Mac)
- **`deploy.ps1`** - PowerShell deployment script (Windows)

### Documentation
- **`DEPLOYMENT_GUIDE.md`** - Step-by-step deployment instructions
- **`KUBERNETES_GUIDE.md`** - Kubernetes operations and troubleshooting
- **`JENKINS_SETUP.md`** - Jenkins configuration guide

## 🚀 Quick Start

### Option 1: Using Bash Script (Linux/Mac)
```bash
chmod +x deploy.sh
export DOCKER_USER="your-docker-username"

# Full deployment
./deploy.sh full

# Or individual steps
./deploy.sh check      # Check prerequisites
./deploy.sh build      # Build Docker image
./deploy.sh push       # Push to Docker Hub
./deploy.sh deploy     # Deploy to Kubernetes
./deploy.sh verify     # Verify deployment
```

### Option 2: Using PowerShell Script (Windows)
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Full deployment
.\deploy.ps1 -Action full -DockerUser "your-docker-username"

# Or individual steps
.\deploy.ps1 -Action check
.\deploy.ps1 -Action build
.\deploy.ps1 -Action push -DockerUser "your-docker-username"
.\deploy.ps1 -Action deploy
.\deploy.ps1 -Action verify
```

### Option 3: Manual Deployment
```bash
# 1. Build Docker image
docker build -t smart-billing-system:1.0 .

# 2. Tag and push to registry
docker tag smart-billing-system:1.0 your-user/smart-billing-system:1.0
docker push your-user/smart-billing-system:1.0

# 3. Create Kubernetes namespace
kubectl apply -f k8s/namespace.yaml

# 4. Deploy application
kubectl apply -f k8s/
```

## 🏗️ Architecture

### Kubernetes Deployment Structure
```
Namespace: smart-billing
├── Deployment: smart-billing (2 replicas)
│   ├── Pod 1 (smart-billing container)
│   └── Pod 2 (smart-billing container)
├── Service: smart-billing-service (NodePort)
│   ├── Port 5900 → NodePort 30900 (GUI)
│   └── Port 8000 → NodePort 30800 (Metrics)
├── ConfigMap: smart-billing-config
├── PersistentVolumeClaim: smart-billing-pvc (1Gi)
└── ServiceAccount: smart-billing
```

### Jenkins Pipeline Stages
```
1. Checkout          → Pull code from Git
2. Build Requirements → Generate requirements.txt
3. Code Quality      → Linting checks
4. Unit Tests        → Run pytest
5. Build Image       → Create Docker image
6. Push Image        → Push to Docker Hub
7. Deploy to K8s     → Apply manifests
8. Verify Deployment → Health checks
```

## 📋 Prerequisites

### System Requirements
- **Docker** v20.10+ 
- **Kubernetes** v1.24+
- **kubectl** configured
- **Jenkins** v2.375+ (for CI/CD)
- **Git** with webhook support

### Docker Hub
- Create account at https://hub.docker.com
- Create personal access token
- Update `docker-credentials` in Jenkins

### Kubernetes Cluster
- Minimum 2 nodes with 1GB RAM each
- StorageClass available (default or custom)
- Ingress controller (optional, for HTTP access)

## 🔧 Configuration

### Update Docker Registry
Edit files and replace `REGISTRY_USER` with your Docker Hub username:

```bash
# In k8s/deployment.yaml
image: YOUR_DOCKER_USER/smart-billing-system:IMAGE_TAG

# In jenkinsFile
REGISTRY_CREDENTIALS = 'your-docker-username'
```

### Customize Kubernetes
Edit `k8s/deployment.yaml`:

```yaml
# Adjust replicas
spec:
  replicas: 3  # Change number of pods

# Modify resource limits
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

### Configure Jenkins
1. Add Docker Hub credentials (ID: `docker-credentials`)
2. Configure Kubernetes cloud in Jenkins
3. Set up GitHub webhook for auto-trigger
4. Create pipeline job pointing to `jenkinsFile`

## 🌐 Accessing the Application

### After Deployment
```bash
# Get the service details
kubectl get svc -n smart-billing

# Port forward method
kubectl port-forward svc/smart-billing-service 5900:5900 -n smart-billing

# Access application
# Local: http://localhost:5900
# NodePort: http://<NODE_IP>:30900
```

## 📊 Monitoring

### View Logs
```bash
# Real-time logs
kubectl logs -f deployment/smart-billing -n smart-billing

# Pod-specific logs
kubectl logs <pod-name> -n smart-billing

# All pods
kubectl logs --all-containers=true -l app=smart-billing -n smart-billing
```

### Check Pod Status
```bash
# Pod details
kubectl describe pod <pod-name> -n smart-billing

# Pod metrics
kubectl top pods -n smart-billing

# Watch pods
kubectl get pods -n smart-billing -w
```

### Database Health
```bash
# Check database
kubectl exec -it <pod-name> -n smart-billing -- sqlite3 /data/s_mart.db ".tables"

# Verify data mount
kubectl exec -it <pod-name> -n smart-billing -- ls -la /data/
```

## 🔄 Updates and Rollbacks

### Update Application
```bash
# Build new version
docker build -t smart-billing-system:2.0 .

# Push to registry
docker push your-user/smart-billing-system:2.0

# Update deployment
kubectl set image deployment/smart-billing \
  smart-billing=your-user/smart-billing-system:2.0 \
  -n smart-billing

# Monitor rollout
kubectl rollout status deployment/smart-billing -n smart-billing
```

### Rollback
```bash
# Check history
kubectl rollout history deployment/smart-billing -n smart-billing

# Rollback to previous
kubectl rollout undo deployment/smart-billing -n smart-billing

# Rollback to specific revision
kubectl rollout undo deployment/smart-billing --to-revision=1 -n smart-billing
```

## 🔒 Security Considerations

- Application runs as non-root user (UID: 1000)
- Read-only root filesystem enabled
- Resource limits enforced
- RBAC configured with minimal permissions
- Pod security policies applied
- Network policies can be added

## 📦 Database

### Persistent Storage
- PVC: 1Gi storage
- Mount point: `/data/`
- Database file: `/data/s_mart.db`

### Backup Database
```bash
# Backup from pod
kubectl cp smart-billing/<pod-name>:/data/s_mart.db ./s_mart.db

# Restore to pod
kubectl cp ./s_mart.db smart-billing/<pod-name>:/data/s_mart.db
```

## ❌ Troubleshooting

### Pod won't start
```bash
# Check logs
kubectl logs <pod-name> -n smart-billing

# Check pod status
kubectl describe pod <pod-name> -n smart-billing

# Check events
kubectl get events -n smart-billing
```

### Image pull fails
```bash
# Verify image exists
docker pull your-user/smart-billing-system:latest

# Check image in deployment
kubectl get deployment smart-billing -n smart-billing -o yaml | grep image
```

### Service not accessible
```bash
# Check endpoints
kubectl get endpoints -n smart-billing

# Test from pod
kubectl exec -it <pod-name> -n smart-billing -- wget localhost:5900
```

### Database connection issues
```bash
# Check PVC
kubectl get pvc -n smart-billing

# Check mount
kubectl exec -it <pod-name> -n smart-billing -- ls -la /data/
```

## 🧹 Cleanup

```bash
# Delete entire deployment
kubectl delete namespace smart-billing

# Delete specific resource
kubectl delete deployment smart-billing -n smart-billing

# Remove local Docker image
docker rmi smart-billing-system:latest
```

## 📚 Documentation Files

- **`DEPLOYMENT_GUIDE.md`** - Comprehensive deployment guide with all steps
- **`JENKINS_SETUP.md`** - Jenkins configuration and pipeline details
- **`KUBERNETES_GUIDE.md`** - Kubernetes operations and troubleshooting
- **`README.md`** - This file

## 🤝 Support

For issues or questions:
1. Check relevant documentation file
2. Review Kubernetes events: `kubectl get events -n smart-billing`
3. Check pod logs: `kubectl logs -f deployment/smart-billing -n smart-billing`
4. Review Jenkins build logs in Jenkins UI

## 📝 Version Information

- **Docker**: Multi-stage build, Python 3.11
- **Python**: 3.11-slim base image
- **Kubernetes**: 1.24+
- **Jenkins**: 2.375+
- **Application**: S_MART Billing System v1.0

## 🎯 Next Steps

1. Update Docker registry credentials
2. Configure Jenkins with GitHub
3. Set up Kubernetes cluster
4. Deploy using provided scripts
5. Configure monitoring and alerts
6. Set up backup strategy

---

**Created**: November 2025
**Project**: S_MART Billing System
**Type**: Tkinter GUI Application with SQLite Database
