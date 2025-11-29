# S_MART Billing System - PowerShell Deployment Script
# Run: .\deploy.ps1 -Action full -DockerUser "your-username"

param(
    [string]$Action = "menu",
    [string]$DockerUser = "your-docker-username",
    [string]$Version = "latest",
    [string]$Namespace = "smart-billing",
    [string]$ImageName = "smart-billing-system"
)

# Color output
function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Green
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

# Check prerequisites
function Check-Prerequisites {
    Write-Info "Checking prerequisites..."
    
    $docker = Get-Command docker -ErrorAction SilentlyContinue
    if (-not $docker) {
        Write-Error "Docker is not installed or not in PATH"
        return $false
    }
    
    $kubectl = Get-Command kubectl -ErrorAction SilentlyContinue
    if (-not $kubectl) {
        Write-Error "kubectl is not installed or not in PATH"
        return $false
    }
    
    Write-Info "Prerequisites check passed"
    return $true
}

# Build Docker image
function Build-Image {
    param([string]$ImageNameTag = $ImageName)
    
    Write-Info "Building Docker image: ${ImageNameTag}:${Version}"
    
    $BuildProcess = Start-Process docker -ArgumentList "build -t ${ImageNameTag}:${Version} -t ${ImageNameTag}:latest ." -NoNewWindow -PassThru -Wait
    
    if ($BuildProcess.ExitCode -eq 0) {
        Write-Info "Docker image built successfully"
        return $true
    } else {
        Write-Error "Failed to build Docker image"
        return $false
    }
}

# Push Docker image
function Push-Image {
    param([string]$User = $DockerUser)
    
    if ($User -eq "your-docker-username") {
        Write-Error "Please set DockerUser parameter"
        return $false
    }
    
    Write-Info "Pushing image to Docker Hub: ${User}/${ImageName}:${Version}"
    
    # Tag image
    $TagProcess = Start-Process docker -ArgumentList "tag ${ImageName}:${Version} ${User}/${ImageName}:${Version}" -NoNewWindow -PassThru -Wait
    if ($TagProcess.ExitCode -ne 0) {
        Write-Error "Failed to tag image"
        return $false
    }
    
    $TagLatestProcess = Start-Process docker -ArgumentList "tag ${ImageName}:${Version} ${User}/${ImageName}:latest" -NoNewWindow -PassThru -Wait
    if ($TagLatestProcess.ExitCode -ne 0) {
        Write-Error "Failed to tag latest image"
        return $false
    }
    
    # Push image
    $PushProcess = Start-Process docker -ArgumentList "push ${User}/${ImageName}:${Version}" -NoNewWindow -PassThru -Wait
    if ($PushProcess.ExitCode -eq 0) {
        Write-Info "Image version pushed successfully"
    } else {
        Write-Error "Failed to push image version"
        return $false
    }
    
    $PushLatestProcess = Start-Process docker -ArgumentList "push ${User}/${ImageName}:latest" -NoNewWindow -PassThru -Wait
    if ($PushLatestProcess.ExitCode -eq 0) {
        Write-Info "Image pushed successfully"
        return $true
    } else {
        Write-Error "Failed to push latest image"
        return $false
    }
}

# Deploy to Kubernetes
function Deploy-Kubernetes {
    param([string]$User = $DockerUser)
    
    Write-Info "Deploying to Kubernetes namespace: ${Namespace}"
    
    # Create namespace
    kubectl create namespace $Namespace --dry-run=client -o yaml | kubectl apply -f -
    
    # Apply manifests
    Write-Info "Applying namespace..."
    kubectl apply -f k8s/namespace.yaml
    
    Write-Info "Applying RBAC..."
    kubectl apply -f k8s/serviceaccount.yaml
    
    Write-Info "Applying ConfigMap..."
    kubectl apply -f k8s/configmap.yaml
    
    Write-Info "Applying PVC..."
    kubectl apply -f k8s/pvc.yaml
    
    Write-Info "Updating deployment image..."
    # Read deployment file
    $DeploymentContent = Get-Content k8s/deployment.yaml -Raw
    
    # Replace placeholders
    $DeploymentContent = $DeploymentContent -replace "REGISTRY_USER", $User
    $DeploymentContent = $DeploymentContent -replace "IMAGE_TAG", $Version
    
    # Write updated deployment
    $DeploymentContent | Set-Content k8s/deployment.yaml
    
    Write-Info "Applying deployment..."
    kubectl apply -f k8s/deployment.yaml
    
    Write-Info "Applying service..."
    kubectl apply -f k8s/service.yaml
    
    Write-Info "Waiting for deployment to be ready (timeout: 5 minutes)..."
    $RolloutProcess = Start-Process kubectl -ArgumentList "rollout", "status", "deployment/smart-billing", "-n", $Namespace, "--timeout=5m" -NoNewWindow -PassThru -Wait
    
    if ($RolloutProcess.ExitCode -eq 0) {
        Write-Info "Deployment completed successfully"
        return $true
    } else {
        Write-Error "Deployment failed"
        return $false
    }
}

# Verify deployment
function Verify-Deployment {
    Write-Info "Verifying deployment..."
    
    Write-Host ""
    Write-Info "Pod Status:"
    kubectl get pods -n $Namespace -o wide
    
    Write-Host ""
    Write-Info "Service Status:"
    kubectl get svc -n $Namespace
    
    Write-Host ""
    Write-Info "Deployment Status:"
    kubectl get deployment -n $Namespace
    
    Write-Host ""
    Write-Info "Accessing the application:"
    Write-Host "  NodePort: http://<NODE_IP>:30900"
    Write-Host "  Port Forward: kubectl port-forward svc/smart-billing-service 5900:5900 -n $Namespace"
}

# Cleanup
function Cleanup {
    Write-Warning "Deleting deployment..."
    kubectl delete namespace $Namespace -ErrorAction SilentlyContinue
    Write-Info "Cleanup completed"
}

# Show menu
function Show-Menu {
    Write-Host ""
    Write-Host "Select an option:"
    Write-Host "1) Check prerequisites"
    Write-Host "2) Build Docker image"
    Write-Host "3) Push Docker image"
    Write-Host "4) Deploy to Kubernetes"
    Write-Host "5) Verify deployment"
    Write-Host "6) Full deployment (all steps)"
    Write-Host "7) Cleanup"
    Write-Host "8) Exit"
    Write-Host ""
}

# Execute action
function Execute-Action {
    param([string]$Action)
    
    switch ($Action.ToLower()) {
        "check" {
            if (Check-Prerequisites) { exit 0 } else { exit 1 }
        }
        "build" {
            if (Build-Image) { exit 0 } else { exit 1 }
        }
        "push" {
            if (Push-Image) { exit 0 } else { exit 1 }
        }
        "deploy" {
            if (Deploy-Kubernetes) { exit 0 } else { exit 1 }
        }
        "verify" {
            Verify-Deployment
        }
        "full" {
            if (-not (Check-Prerequisites)) { exit 1 }
            if (-not (Build-Image)) { exit 1 }
            if (-not (Push-Image)) { exit 1 }
            if (-not (Deploy-Kubernetes)) { exit 1 }
            Verify-Deployment
            Write-Info "Full deployment completed"
        }
        "cleanup" {
            Cleanup
        }
        "menu" {
            $continue = $true
            while ($continue) {
                Show-Menu
                $choice = Read-Host "Enter your choice [1-8]"
                
                switch ($choice) {
                    "1" { Check-Prerequisites }
                    "2" { Build-Image }
                    "3" { Push-Image }
                    "4" { Deploy-Kubernetes }
                    "5" { Verify-Deployment }
                    "6" {
                        Check-Prerequisites
                        Build-Image
                        Push-Image
                        Deploy-Kubernetes
                        Verify-Deployment
                    }
                    "7" { Cleanup }
                    "8" {
                        Write-Info "Exiting..."
                        $continue = $false
                    }
                    default {
                        Write-Error "Invalid option. Please try again."
                    }
                }
            }
        }
        default {
            Write-Error "Usage: .\deploy.ps1 -Action {check|build|push|deploy|verify|full|cleanup|menu} -DockerUser <username> -Version <version>"
            exit 1
        }
    }
}

# Main script
Write-Host "=== S_MART Billing System Deployment ===" -ForegroundColor Cyan
Execute-Action $Action
