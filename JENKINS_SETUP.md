# Jenkins Pipeline CI/CD Configuration

This document explains the Jenkins pipeline stages and how to set up Jenkins for the S_MART Billing System.

## Pipeline Stages

### 1. **Checkout**
- Pulls code from Git repository
- Triggered on push/pull request events

### 2. **Build Requirements**
- Generates `requirements.txt` from installed Python packages
- Ensures all dependencies are captured

### 3. **Code Quality & Linting**
- Runs Flake8 for Python code quality
- Non-blocking stage (warnings don't fail build)

### 4. **Unit Tests**
- Runs pytest for unit testing
- Creates test infrastructure

### 5. **Build Docker Image**
- Creates Docker image with tag `{BUILD_NUMBER}`
- Tags as both versioned and `latest`

### 6. **Push Docker Image**
- Logs into Docker Hub
- Pushes image to registry
- Cleans up credentials

### 7. **Deploy to Kubernetes**
- Updates deployment manifest with image tag
- Applies all Kubernetes manifests
- Waits for rollout completion (5 min timeout)

### 8. **Verify Deployment**
- Checks pod status
- Displays service endpoints
- Confirms deployment health

## Jenkins Setup

### Install Required Plugins
1. Go to Jenkins > Manage Jenkins > Plugin Manager
2. Install these plugins:
   - Docker Pipeline
   - Kubernetes
   - Git
   - Pipeline
   - CloudBees Docker Build and Publish
   - Email Extension
   - AnsiColor

### Configure Docker Credentials
1. Jenkins > Credentials > System > Global credentials
2. Add credentials:
   - **Kind**: Username with password
   - **Username**: Your Docker Hub username
   - **Password**: Your Docker Hub password (or token)
   - **ID**: `docker-credentials`
   - **Description**: Docker Hub credentials

### Configure Kubernetes Credentials
1. Jenkins > Manage Jenkins > Configure System
2. Find "Cloud" section
3. Add Kubernetes cloud:
   - **Name**: kubernetes
   - **Kubernetes URL**: Your K8s API endpoint
   - **Kubernetes Namespace**: smart-billing
   - **Jenkins URL**: Your Jenkins server URL

### Configure Pipeline Job
1. Create New > Pipeline
2. **General**:
   - Display name: S_MART Billing CI/CD
   - Discard old builds: Keep last 10 builds
3. **Build Triggers**:
   - Check: GitHub hook trigger for GITScm polling
4. **Pipeline**:
   - Definition: Pipeline script from SCM
   - SCM: Git
     - Repository URL: `https://github.com/YOUR_REPO.git`
     - Credentials: (Add GitHub credentials)
     - Branch: */main
   - Script Path: jenkinsFile

### GitHub Webhook Setup
1. Go to GitHub repository > Settings > Webhooks
2. Add webhook:
   - **Payload URL**: `http://your-jenkins-server:8080/github-webhook/`
   - **Content type**: application/json
   - **Events**: Push events
   - Check: Active

## Environment Variables in Pipeline

```
REGISTRY = docker.io
REGISTRY_CREDENTIALS = Your Docker Hub username
IMAGE_NAME = smart-billing-system
IMAGE_TAG = ${BUILD_NUMBER}
KUBECONFIG = Path to kubeconfig
DOCKER_IMAGE = Full image reference
```

## Accessing Pipeline Dashboard
- Dashboard: `http://jenkins-server/job/smart-billing-deploy/`
- View logs: Click build number > Console Output
- View artifacts: Click build number > Artifacts
- Trigger manually: Click "Build Now"

## Troubleshooting Pipeline Issues

### Docker Push Fails
- Check credentials are correct
- Verify Docker Hub account isn't restricted
- Check network connectivity to registry

### Kubernetes Deployment Fails
- Verify kubeconfig path is correct
- Check namespace exists: `kubectl get namespace smart-billing`
- Verify service account has proper RBAC

### Image Pull Fails
- Ensure image exists in registry
- Check image pull policy
- Verify registry credentials in Kubernetes

### Rollout Timeout
- Check pod logs: `kubectl logs -f <pod-name> -n smart-billing`
- Increase timeout in deployment stage if needed
- Verify resource availability in cluster

## Monitoring Pipeline Execution

### Real-time Monitoring
1. Open job page in Jenkins
2. Click ongoing build number
3. View "Console Output" for real-time logs

### Build History
- Track all builds and their status
- View logs from completed builds
- Check artifact archives

### Email Notifications
To add email on failure:
1. Add to post-failure section in jenkinsFile:
```groovy
mail to: 'team@example.com',
      subject: "Pipeline Failed: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
      body: "Build failed. Check console at ${env.BUILD_URL}"
```

## Advanced Configuration

### Enable Email Notifications
1. Jenkins > Manage Jenkins > Configure System
2. Find "Email Notification"
3. Set SMTP server and credentials
4. Test configuration

### Set Resource Limits
Update jenkinsFile agent section:
```groovy
agent {
  kubernetes {
    yaml '''
    apiVersion: v1
    kind: Pod
    spec:
      containers:
      - name: docker
        image: docker:latest
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
    '''
  }
}
```

### Parallel Stages
Modify jenkinsFile to run multiple stages in parallel:
```groovy
parallel {
  stage('Build') {
    steps {
      // build steps
    }
  }
  stage('Test') {
    steps {
      // test steps
    }
  }
}
```

## Manual Pipeline Execution
```bash
# Trigger via curl
curl -X POST http://jenkins-user:token@jenkins-server:8080/job/smart-billing-deploy/build

# With parameters
curl -X POST http://jenkins-server:8080/job/smart-billing-deploy/build?BUILD_NUMBER=v1.1
```
