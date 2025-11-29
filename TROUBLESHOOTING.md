# Troubleshooting and FAQ

## Common Issues and Solutions

### 1. Docker Image Build Fails

**Error**: `E: Unable to locate package python3-tk`

**Solution**:
```dockerfile
# Make sure to update package lists first
RUN apt-get update && apt-get install -y python3-tk
```

**Error**: `COPY failed: file not found`

**Solution**:
- Ensure `requirements.txt` exists in project root
- Check `.dockerignore` isn't excluding necessary files
- Verify working directory in Dockerfile

---

### 2. Docker Push to Registry Fails

**Error**: `denied: requested access to the resource is denied`

**Solution**:
```bash
# Login to Docker Hub
docker login

# Verify credentials
# Tag image with your username
docker tag smart-billing-system YOUR_USERNAME/smart-billing-system
docker push YOUR_USERNAME/smart-billing-system
```

**Error**: `no basic auth credentials`

**Solution**:
- Jenkins: Add credentials with ID `docker-credentials`
- Verify Docker Hub token is valid
- Check `~/.docker/config.json` has valid credentials

---

### 3. Kubernetes Pod Issues

**Pod Status**: `ImagePullBackOff`

**Solution**:
```bash
# Check image exists and is correct tag
docker pull your-username/smart-billing-system:latest

# Check deployment image specification
kubectl get deployment smart-billing -n smart-billing -o yaml | grep image

# Update image if needed
kubectl set image deployment/smart-billing \
  smart-billing=your-username/smart-billing-system:latest \
  -n smart-billing
```

**Pod Status**: `CrashLoopBackOff`

**Solution**:
```bash
# Check pod logs
kubectl logs <pod-name> -n smart-billing

# Check previous logs (if crashed)
kubectl logs <pod-name> --previous -n smart-billing

# Describe pod for detailed error
kubectl describe pod <pod-name> -n smart-billing

# Check resource availability
kubectl describe node <node-name>
```

**Pod Status**: `Pending`

**Solution**:
```bash
# Check PVC is bound
kubectl get pvc -n smart-billing
kubectl describe pvc smart-billing-pvc -n smart-billing

# Check node resources
kubectl describe nodes

# Check resource requests vs available
kubectl get resourcequota -n smart-billing
```

---

### 4. Service Not Accessible

**Issue**: Cannot connect to application

**Solution**:
```bash
# Check service endpoints
kubectl get endpoints -n smart-billing

# Check service configuration
kubectl describe svc smart-billing-service -n smart-billing

# Test connectivity from pod
kubectl exec -it <pod-name> -n smart-billing -- wget localhost:5900

# Use port-forward
kubectl port-forward svc/smart-billing-service 5900:5900 -n smart-billing
```

**Error**: `Connection refused`

**Solution**:
```bash
# Verify pods are running
kubectl get pods -n smart-billing

# Check pod logs for application startup errors
kubectl logs deployment/smart-billing -n smart-billing

# Check if service selector matches pod labels
kubectl get pods -n smart-billing --show-labels
kubectl get svc smart-billing-service -n smart-billing -o yaml | grep selector
```

---

### 5. Database Issues

**Error**: `database is locked`

**Solution**:
```bash
# Restart affected pods
kubectl rollout restart deployment/smart-billing -n smart-billing

# Or delete single pod
kubectl delete pod <pod-name> -n smart-billing
```

**Error**: `no such table` or database errors

**Solution**:
```bash
# Check if database file exists
kubectl exec -it <pod-name> -n smart-billing -- ls -la /data/

# Check PVC mount
kubectl exec -it <pod-name> -n smart-billing -- df -h

# Verify database creation
kubectl exec -it <pod-name> -n smart-billing -- \
  sqlite3 /data/s_mart.db ".tables"

# Recreate database if necessary
kubectl exec -it <pod-name> -n smart-billing -- python create_db.py
```

**Issue**: Database grows too large

**Solution**:
```bash
# Check database size
kubectl exec -it <pod-name> -n smart-billing -- du -h /data/s_mart.db

# Backup and compact database
kubectl exec -it <pod-name> -n smart-billing -- \
  sqlite3 /data/s_mart.db "VACUUM;"
```

---

### 6. Jenkins Pipeline Failures

**Stage Failure**: Checkout

**Solution**:
```bash
# Check Git credentials in Jenkins
# Verify repository URL
# Check webhook configuration
# Test Git access: git clone YOUR_REPO_URL
```

**Stage Failure**: Build Docker Image

**Solution**:
```bash
# Check Dockerfile exists in root
# Verify requirements.txt is present
# Build locally to debug:
docker build -t test . --progress=plain
```

**Stage Failure**: Push to Registry

**Solution**:
```bash
# Verify Docker credentials in Jenkins
# Check registry URL
# Test locally:
docker login
docker push your-user/smart-billing-system:latest
```

**Stage Failure**: Deploy to Kubernetes

**Solution**:
```bash
# Verify kubeconfig path in Jenkins
# Check RBAC permissions
# Test kubectl access:
kubectl get nodes

# Verify deployment manifests
kubectl apply -f k8s/ --dry-run=client -o yaml
```

---

### 7. Performance Issues

**Issue**: Pods consuming high memory

**Solution**:
```bash
# Check actual memory usage
kubectl top pods -n smart-billing

# Increase memory limit if needed
kubectl edit deployment smart-billing -n smart-billing
# Update resources.limits.memory

# Or set via command:
kubectl set resources deployment smart-billing \
  --limits=memory=1Gi -n smart-billing
```

**Issue**: Slow application response

**Solution**:
```bash
# Check pod logs for errors
kubectl logs deployment/smart-billing -n smart-billing

# Check database performance
kubectl exec -it <pod-name> -n smart-billing -- \
  sqlite3 /data/s_mart.db "EXPLAIN QUERY PLAN SELECT * FROM customer;"

# Monitor resource usage
kubectl top pods -n smart-billing
```

---

### 8. Network Issues

**Error**: `connection refused` on localhost:5900

**Solution**:
```bash
# Verify port-forward is active
kubectl port-forward svc/smart-billing-service 5900:5900 -n smart-billing

# Try different port if 5900 is in use
kubectl port-forward svc/smart-billing-service 6000:5900 -n smart-billing
# Access: localhost:6000
```

**Error**: Cannot reach from external IP

**Solution**:
```bash
# Use NodePort instead of ClusterIP
# Check firewall rules
# Verify service type:
kubectl get svc smart-billing-service -n smart-billing

# Get NodePort details:
kubectl get svc smart-billing-service -n smart-billing -o wide
```

---

## Useful Debugging Commands

```bash
# General cluster info
kubectl cluster-info
kubectl get nodes
kubectl get namespaces

# Namespace diagnostics
kubectl get all -n smart-billing
kubectl describe namespace smart-billing

# Pod diagnostics
kubectl get pods -n smart-billing -o wide
kubectl describe pod <pod-name> -n smart-billing
kubectl logs <pod-name> -n smart-billing
kubectl logs <pod-name> --previous -n smart-billing
kubectl exec -it <pod-name> -n smart-billing -- /bin/bash

# Service diagnostics
kubectl get svc -n smart-billing
kubectl describe svc smart-billing-service -n smart-billing
kubectl get endpoints -n smart-billing

# Deployment diagnostics
kubectl get deployment -n smart-billing
kubectl describe deployment smart-billing -n smart-billing
kubectl rollout history deployment/smart-billing -n smart-billing

# Storage diagnostics
kubectl get pvc -n smart-billing
kubectl describe pvc smart-billing-pvc -n smart-billing
kubectl get pv

# Events and troubleshooting
kubectl get events -n smart-billing
kubectl get events -n smart-billing --sort-by='.lastTimestamp'

# Resource usage
kubectl top nodes
kubectl top pods -n smart-billing

# Repair commands
kubectl delete pod <pod-name> -n smart-billing
kubectl rollout restart deployment/smart-billing -n smart-billing
```

---

## Prevention Tips

1. **Always test Docker image locally**:
   ```bash
   docker build -t test:latest .
   docker run -it test:latest /bin/bash
   ```

2. **Use proper resource limits** to prevent pod eviction

3. **Configure health checks** (liveness and readiness probes)

4. **Use namespaces** to isolate deployments

5. **Enable RBAC** for security

6. **Regular backups** of database:
   ```bash
   kubectl cp smart-billing/<pod>:/data/s_mart.db ./backup.db
   ```

7. **Monitor resource usage** regularly:
   ```bash
   watch kubectl top pods -n smart-billing
   ```

8. **Keep images up to date** with security patches

---

## Contact and Escalation

If issues persist:
1. Collect all relevant logs and describe the issue
2. Provide cluster information and pod details
3. Check if this is a known limitation
4. Consider consulting Kubernetes documentation
5. Review Docker best practices

---

**Last Updated**: November 2025
