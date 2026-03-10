param(
    [string]$Version = "1.0.0",
    [string]$Registry = "ghcr.io/jashwanthmu"
)

Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║         TerraSecure Docker Image Builder                     ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "Version:  $Version" -ForegroundColor Yellow
Write-Host "Registry: $Registry" -ForegroundColor Yellow
Write-Host ""

Write-Host " Building production model..." -ForegroundColor Green
python scripts\build_production_model.py

if ($LASTEXITCODE -ne 0) {
    Write-Host " Model build failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host " Building Docker image..." -ForegroundColor Green
docker build `
    --build-arg VERSION=$Version `
    --tag terrasecure:latest `
    --tag terrasecure:$Version `
    --tag ${Registry}/terrasecure:latest `
    --tag ${Registry}/terrasecure:$Version `
    .

if ($LASTEXITCODE -ne 0) {
    Write-Host " Docker build failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host " Testing Docker image..." -ForegroundColor Green
docker run --rm terrasecure:latest --version

Write-Host ""
Write-Host " Image Info:" -ForegroundColor Cyan
docker images terrasecure:latest

$push = Read-Host "Push to registry? (y/n)"
if ($push -eq "y" -or $push -eq "Y") {
    Write-Host " Pushing to registry..." -ForegroundColor Green
    docker push ${Registry}/terrasecure:latest
    docker push ${Registry}/terrasecure:$Version
    Write-Host " Pushed successfully!" -ForegroundColor Green
}

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                  BUILD COMPLETE                               ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "Usage Examples:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  # Scan directory"
Write-Host "  docker run -v ${PWD}:/scan terrasecure:latest /scan"
Write-Host ""
Write-Host "  # Scan with JSON output"
Write-Host "  docker run -v ${PWD}:/scan terrasecure:latest /scan --format json"
Write-Host ""
Write-Host "  # Scan and fail on critical"
Write-Host "  docker run -v ${PWD}:/scan terrasecure:latest /scan --fail-on critical"
Write-Host ""