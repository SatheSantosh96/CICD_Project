# Jenkins Setup Guide - S_MART Billing System CI/CD

## Complete Step-by-Step Setup from Scratch

### STEP 1: Install Required Jenkins Plugins

Jenkins needs these plugins to work with Docker and Kubernetes:

1. **Go to Jenkins Dashboard**
   - URL: `http://your-jenkins-server:8080`
   - Click "Manage Jenkins" → "Plugin Manager"

2. **Install These Plugins** (Manage Jenkins → Plugin Manager → Available Tab):
   - Docker Pipeline
   - Kubernetes
   - Git
   - Pipeline
   - CloudBees Docker Build and Publish
   - GitHub Integration
   - AnsiColor
   - Email Extension
   - Blue Ocean (optional, for better UI)

**How to Install:**
- Search for plugin name
- Check the checkbox
- Click "Install without restart" or "Download now and install after restart"
- Wait for installation to complete

---

### STEP 2: Add Docker Hub Credentials to Jenkins

This allows Jenkins to push images to Docker Hub.

1. **Navigate to Credentials**
   - Jenkins Dashboard → Credentials → System → Global credentials

2. **Add Credentials**
   - Click "Add Credentials" (left sidebar)
   - Kind: **Username with password**
   - Username: `your-docker-hub-username`
   - Password: `your-docker-hub-password` (or personal access token)
   - ID: `docker-credentials` (IMPORTANT - must match Jenkinsfile)
   - Description: Docker Hub credentials
   - Click "Create"

**Note**: For security, use a Personal Access Token instead of password:
- Go to Docker Hub Settings → Security → New Access Token
- Use the token as password in Jenkins

---

### STEP 3: Create New Pipeline Job

1. **Create New Job**
   - Jenkins Dashboard → Click "New Item"
   - Job name: `smart-billing-deploy`
   - Select: "Pipeline"
   - Click "OK"

2. **Configure General Settings**
   - Display name: `S_MART Billing CI/CD`
   - Description: `Automated deployment pipeline for S_MART Billing System`
   - Discard old builds: ✓ Check
     - Max # of builds to keep: 10
     - Max # of builds to keep with artifacts: 5

3. **Configure Build Triggers**
   - ✓ Check "GitHub hook trigger for GITScm polling"
   - This enables automatic builds on Git push

4. **Configure Pipeline**
   - Definition: **Pipeline script from SCM**
   - SCM: **Git**
   
5. **Git Configuration**
   - Repository URL: `https://github.com/SatheSantosh96/CICD_Project.git`
   - Credentials: (Add GitHub credentials if needed)
     - Kind: Username with password
     - Username: Your GitHub username
     - Password: Your GitHub personal access token
     - ID: `github-credentials`
   - Branches to build: `*/main` (or your branch)
   - Script Path: `Jenkinsfile` (must be exact name and case)

6. **Click "Save"**

---

### STEP 4: Add GitHub Webhook for Auto-Trigger

This allows Jenkins to automatically build when you push code to GitHub.

1. **In Your GitHub Repository**
   - Go to Settings → Webhooks
   - Click "Add webhook"

2. **Configure Webhook**
   - Payload URL: `http://your-jenkins-server:8080/github-webhook/`
   - Content type: `application/json`
   - Events: Select "Just the push event"
   - ✓ Check "Active"
   - Click "Add webhook"

3. **Test Webhook**
   - GitHub will show a green checkmark if Jenkins received it
   - If red ✗, check your Jenkins URL is accessible

---

### STEP 5: Configure Kubernetes in Jenkins (Optional but Recommended)

This allows Jenkins to deploy to your Kubernetes cluster.

1. **Go to Jenkins Configuration**
   - Manage Jenkins → Configure System
   - Scroll down to "Cloud" section
   - Click "New cloud" → Kubernetes

2. **Configure Kubernetes**
   - Name: `kubernetes`
   - Kubernetes URL: Your cluster API endpoint
   - Kubernetes Namespace: `smart-billing`
   - Jenkins URL: Your Jenkins server URL

3. **Add Kubernetes Credentials**
   - Click "Add" next to Kubernetes credentials
   - Use your kubeconfig file

---

### STEP 6: Test Your Pipeline

1. **Manual Trigger**
   - Go to your job: `smart-billing-deploy`
   - Click "Build Now"
   - Watch the build in real-time under "Build History"

2. **Monitor Build**
   - Click on build number → "Console Output"
   - Watch all 8 stages execute:
     1. Checkout
     2. Build Requirements
     3. Code Quality
     4. Unit Tests
     5. Build Docker Image
     6. Push Docker Image
     7. Deploy to Kubernetes
     8. Verify Deployment

3. **Expected Results**
   - ✅ All stages complete with green status
   - ✅ Docker image in Docker Hub
   - ✅ Pods running in Kubernetes
   - ✅ Service accessible at http://<node-ip>:30900

---

## Troubleshooting Jenkins Setup

### Jenkins Can't Find Jenkinsfile
**Error**: `Unable to find Jenkinsfile`
**Solution**:
- Ensure filename is exactly `Jenkinsfile` (capital J, capital F)
- File must be in repository root directory
- Check git branch is correct (*/main)

### Docker Credentials Fail
**Error**: `denied: requested access to the resource is denied`
**Solution**:
- Verify credentials ID matches: `docker-credentials`
- Test credentials work locally: `docker login`
- Use Personal Access Token, not password
- Check token hasn't expired

### Kubernetes Deployment Fails
**Error**: `Unable to connect to Kubernetes`
**Solution**:
- Verify kubeconfig path in Jenkins
- Check Kubernetes namespace exists: `kubectl get ns smart-billing`
- Verify Jenkins has kubectl installed
- Test kubectl from Jenkins: `kubectl cluster-info`

### GitHub Webhook Not Triggering
**Error**: Build not triggered on push
**Solution**:
- Verify webhook URL is correct in GitHub settings
- Check GitHub can reach your Jenkins server
- Enable "GitHub hook trigger for GITScm polling" in job
- Test manually: Click "Build Now"

### Permission Denied Errors
**Error**: Permission denied when building
**Solution**:
- Verify Jenkins user has access to Docker socket
- Check kubeconfig permissions
- Verify GitHub credentials have repo access
- Check Docker credentials in Jenkins

---

## Jenkins Job Configuration Summary

| Setting | Value |
|---------|-------|
| Job Type | Pipeline |
| SCM | Git |
| Repository | https://github.com/SatheSantosh96/CICD_Project.git |
| Branch | */main |
| Script Path | Jenkinsfile |
| Triggers | GitHub hook |
| Docker Credentials ID | docker-credentials |

---

## Environment Variables in Jenkinsfile

These are automatically set and used:

```
REGISTRY = docker.io
REGISTRY_CREDENTIALS = docker-credentials (your Docker username)
IMAGE_NAME = smart-billing-system
IMAGE_TAG = ${BUILD_NUMBER}
KUBECONFIG = /var/lib/jenkins/.kube/config
DOCKER_IMAGE = Full image reference
```

---

## Jenkins Pipeline Stages Explained

### Stage 1: Checkout
```groovy
checkout scm  // Pulls code from Git
```
- Downloads latest code from your GitHub repository

### Stage 2: Build Requirements
```groovy
python3 -m pip freeze > requirements.txt
```
- Generates list of Python dependencies

### Stage 3: Code Quality & Linting
```groovy
flake8 *.py --count --select=E9,F63,F7,F82
```
- Checks code quality (non-blocking)

### Stage 4: Unit Tests
```groovy
pytest tests/
```
- Runs unit tests

### Stage 5: Build Docker Image
```groovy
docker build -t smart-billing-system:${BUILD_NUMBER}
```
- Creates Docker image locally

### Stage 6: Push Docker Image
```groovy
docker push your-user/smart-billing-system:${BUILD_NUMBER}
```
- Pushes to Docker Hub

### Stage 7: Deploy to Kubernetes
```groovy
kubectl apply -f k8s/
```
- Deploys to Kubernetes cluster

### Stage 8: Verify Deployment
```groovy
kubectl rollout status deployment/smart-billing
```
- Confirms deployment is healthy

---

## Quick Reference Commands

### Check Jenkins Status
```bash
# Jenkins service status
sudo systemctl status jenkins

# View Jenkins logs
sudo tail -f /var/log/jenkins/jenkins.log

# Restart Jenkins
sudo systemctl restart jenkins
```

### Check Plugins
```bash
# SSH into Jenkins container/server
# Navigate to: http://localhost:8080/pluginManager

# Or check installed plugins via CLI
java -jar jenkins-cli.jar -s http://localhost:8080 list-plugins
```

### Manual Build Trigger
```bash
# Trigger build via curl
curl -X POST http://jenkins-user:token@jenkins-server:8080/job/smart-billing-deploy/build
```

---

## Security Best Practices

1. **Never commit credentials** to GitHub
2. **Use Personal Access Tokens** instead of passwords
3. **Restrict webhook** to specific IPs if possible
4. **Use HTTPS** for Jenkins URL
5. **Enable authentication** on Jenkins
6. **Regularly rotate** Docker Hub tokens
7. **Use Jenkins secrets** for sensitive data

---

## Next Steps After Setup

1. ✅ Plugins installed
2. ✅ Credentials configured
3. ✅ Job created
4. ✅ Webhook enabled
5. ✅ Test manual build
6. → Make a code change and push to GitHub
7. → Verify automatic build triggers
8. → Monitor Kubernetes deployment
9. → Access application at http://<node-ip>:30900

---

## Support

If you encounter issues:
1. Check Jenkins logs: `http://localhost:8080/log/all`
2. Review job console output: Job → Build → Console Output
3. Verify all prerequisites met
4. Check GitHub webhook delivery: Settings → Webhooks → Recent Deliveries
5. Consult TROUBLESHOOTING.md for detailed solutions

---

**Ready to deploy!** 🚀
