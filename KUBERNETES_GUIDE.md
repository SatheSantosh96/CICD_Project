# Kubernetes Deployment Guide

Complete guide for deploying S_MART Billing System on Kubernetes.

## Kubernetes Architecture

### Components
1. **Namespace**: `smart-billing` - Isolated environment
2. **Deployment**: 2 replicas with auto-restart
3. **Service**: NodePort and Headless services for access
4. **ConfigMap**: Application configuration
5. **PersistentVolumeClaim**: Database storage
6. **ServiceAccount**: RBAC and pod identity
7. **Ingress**: HTTP/HTTPS routing (optional)

## Prerequisites

### Cluster Requirements
- Kubernetes 1.24 or higher
- At least 2 nodes (1GB RAM each)
- kubectl configured
- PV provisioner or default StorageClass

### Check Cluster Status
```bash
kubectl cluster-info
kubectl get nodes
kubectl get storageclasses
```

## Deployment Process

### Step 1: Create Namespace and RBAC
```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Create service account and roles
kubectl apply -f k8s/serviceaccount.yaml

# Verify
kubectl get serviceaccount -n smart-billing
kubectl get role -n smart-billing
```

### Step 2: Create Storage
```bash
# Create persistent volume claim
kubectl apply -f k8s/pvc.yaml

# Verify
kubectl get pvc -n smart-billing
kubectl get pv
```

### Step 3: Configure Application
```bash
# Create ConfigMap
kubectl apply -f k8s/configmap.yaml

# Verify
kubectl get configmap -n smart-billing
kubectl get configmap smart-billing-config -n smart-billing -o yaml
```

### Step 4: Deploy Application
```bash
# Deploy pods
kubectl apply -f k8s/deployment.yaml

# Verify
kubectl get deployment -n smart-billing
kubectl get pods -n smart-billing
```

### Step 5: Expose Service
```bash
# Create service
kubectl apply -f k8s/service.yaml

# Verify
kubectl get svc -n smart-billing
kubectl get endpoints -n smart-billing
```

### Step 6: Verify Health
```bash
# Check pod status
kubectl get pods -n smart-billing -o wide

# Check pod details
kubectl describe pod -n smart-billing

# Check logs
kubectl logs deployment/smart-billing -n smart-billing

# Wait for ready
kubectl wait --for=condition=ready pod -l app=smart-billing -n smart-billing --timeout=300s
```

## Accessing the Application

### Method 1: NodePort
```bash
# Get node IP and port
kubectl get svc smart-billing-service -n smart-billing
# Port: 30900 (GUI), 30800 (Metrics)
# Access: http://<NODE_IP>:30900
```

### Method 2: Port Forwarding
```bash
# Local port forwarding
kubectl port-forward svc/smart-billing-service 5900:5900 -n smart-billing

# Access: localhost:5900
```

### Method 3: Ingress (Advanced)
```bash
# Requires ingress controller (nginx, traefik, etc.)
# Hostname: billing.example.com (configure in ingress.yaml)
# Update /etc/hosts or DNS accordingly
```

## Monitoring and Debugging

### View Logs
```bash
# Current logs
kubectl logs deployment/smart-billing -n smart-billing

# Tail logs
kubectl logs -f deployment/smart-billing -n smart-billing

# Logs from specific pod
kubectl logs <POD_NAME> -n smart-billing

# Previous logs (if crashed)
kubectl logs <POD_NAME> --previous -n smart-billing

# Last N lines
kubectl logs deployment/smart-billing -n smart-billing --tail=50
```

### Inspect Pods
```bash
# Get pod details
kubectl describe pod <POD_NAME> -n smart-billing

# Get pod YAML
kubectl get pod <POD_NAME> -n smart-billing -o yaml

# Execute command in pod
kubectl exec -it <POD_NAME> -n smart-billing -- /bin/bash

# Check database
kubectl exec -it <POD_NAME> -n smart-billing -- sqlite3 /data/s_mart.db ".tables"
```

### Resource Usage
```bash
# Pod resource usage (requires metrics-server)
kubectl top pods -n smart-billing

# Node resource usage
kubectl top nodes

# Describe resource requests/limits
kubectl describe node <NODE_NAME>
```

## Scaling and Updates

### Manual Scaling
```bash
# Scale to N replicas
kubectl scale deployment smart-billing --replicas=3 -n smart-billing

# Check scaling status
kubectl get deployment smart-billing -n smart-billing
kubectl get hpa -n smart-billing
```

### Rolling Updates
```bash
# Update image tag
kubectl set image deployment/smart-billing \
  smart-billing=docker-user/smart-billing-system:2.0 \
  -n smart-billing

# Check rollout status
kubectl rollout status deployment/smart-billing -n smart-billing

# View rollout history
kubectl rollout history deployment/smart-billing -n smart-billing

# Rollback to previous version
kubectl rollout undo deployment/smart-billing -n smart-billing

# Rollback to specific revision
kubectl rollout undo deployment/smart-billing --to-revision=1 -n smart-billing
```

### Update Configuration
```bash
# Edit deployment directly
kubectl edit deployment smart-billing -n smart-billing

# Update ConfigMap
kubectl edit configmap smart-billing-config -n smart-billing

# Trigger pod restart
kubectl rollout restart deployment/smart-billing -n smart-billing
```

## Backup and Restore

### Backup Database
```bash
# Copy database from pod
kubectl cp smart-billing/<POD_NAME>:/data/s_mart.db ./s_mart.db

# Backup entire namespace
kubectl get all -n smart-billing -o yaml > smart-billing-backup.yaml
```

### Restore Database
```bash
# Copy database to pod
kubectl cp ./s_mart.db smart-billing/<POD_NAME>:/data/s_mart.db

# Restart pods to use restored DB
kubectl rollout restart deployment/smart-billing -n smart-billing
```

## Troubleshooting

### Pod CrashLoopBackOff
```bash
# Check logs
kubectl logs <POD_NAME> -n smart-billing

# Check previous logs
kubectl logs <POD_NAME> --previous -n smart-billing

# Describe pod for events
kubectl describe pod <POD_NAME> -n smart-billing

# Check resource limits
kubectl describe node <NODE_NAME>
```

### ImagePullBackOff
```bash
# Verify image exists and is accessible
docker pull docker-user/smart-billing-system:TAG

# Check image pull secrets
kubectl get secrets -n smart-billing

# Check if image tag is correct in deployment
kubectl get deployment smart-billing -n smart-billing -o yaml | grep image
```

### Database Connection Issues
```bash
# Check PVC mount
kubectl exec -it <POD_NAME> -n smart-billing -- ls -la /data/

# Check database file
kubectl exec -it <POD_NAME> -n smart-billing -- file /data/s_mart.db

# Test database access
kubectl exec -it <POD_NAME> -n smart-billing -- python3 -c \
  "import sqlite3; con=sqlite3.connect('/data/s_mart.db'); print('DB OK')"
```

### Service Not Accessible
```bash
# Check service endpoints
kubectl get endpoints -n smart-billing

# Check service configuration
kubectl describe svc smart-billing-service -n smart-billing

# Test connectivity from pod
kubectl exec -it <POD_NAME> -n smart-billing -- \
  wget -O- http://smart-billing-service:5900
```

## Cleanup

### Delete Everything
```bash
# Delete namespace (deletes all resources)
kubectl delete namespace smart-billing

# Delete specific resource
kubectl delete deployment smart-billing -n smart-billing
kubectl delete svc smart-billing-service -n smart-billing
```

## Performance Optimization

### Resource Limits
Adjust in `deployment.yaml`:
```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

### Horizontal Pod Autoscaling
```bash
# Create HPA
kubectl autoscale deployment smart-billing \
  --min=2 --max=5 \
  --cpu-percent=80 \
  -n smart-billing

# View HPA
kubectl get hpa -n smart-billing
```

### Pod Disruption Budget
```bash
# Ensure minimum pods during disruptions
kubectl apply -f - <<EOF
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: smart-billing-pdb
  namespace: smart-billing
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app: smart-billing
EOF
```

## Advanced Topics

### Network Policies
```yaml
# Restrict traffic to pods
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: smart-billing-netpol
  namespace: smart-billing
spec:
  podSelector:
    matchLabels:
      app: smart-billing
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
```

### StatefulSet (for persistent sessions)
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: smart-billing-stateful
  namespace: smart-billing
spec:
  serviceName: smart-billing-headless
  replicas: 2
  # ... (similar spec as deployment)
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 1Gi
```
