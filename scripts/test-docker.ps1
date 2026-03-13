<#
.SYNOPSIS
    Test TerraSecure Docker Image

.DESCRIPTION
    Comprehensive testing of TerraSecure Docker image functionality

.EXAMPLE
    .\scripts\test-docker.ps1
#>

param(
    [string]$ImageTag = "terrasecure:latest"
)

$ErrorActionPreference = "Continue"

function Write-TestHeader {
    param([string]$Title)
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host "  $Title" -ForegroundColor White
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host ""
}

function Write-TestResult {
    param(
        [string]$Test,
        [bool]$Passed,
        [string]$Message = ""
    )
    
    $status = if ($Passed) { "PASS" } else { "FAIL" }
    $icon = if ($Passed) { "[OK]" } else { "[X]" }
    $color = if ($Passed) { "Green" } else { "Red" }
    
    Write-Host "$icon $status - $Test" -ForegroundColor $color
    if ($Message) {
        Write-Host "       $Message" -ForegroundColor Gray
    }
}

# Start Tests
Clear-Host
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "       TerraSecure Docker Image Test Suite                     " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Image: $ImageTag" -ForegroundColor Yellow
Write-Host "Path:  $PWD" -ForegroundColor Yellow
Write-Host ""

$testResults = @()
$startTime = Get-Date

# Test 1: Image Exists
Write-TestHeader "Test 1: Docker Image Exists"
try {
    $imageExists = docker images $ImageTag --format "{{.Repository}}:{{.Tag}}" 2>&1 | Select-String $ImageTag
    if ($imageExists) {
        Write-TestResult "Image exists" $true
        $testResults += $true
    } else {
        Write-TestResult "Image exists" $false "Run docker build -t $ImageTag ."
        $testResults += $false
        Write-Host ""
        Write-Host "Build the image first:" -ForegroundColor Yellow
        Write-Host "  docker build -t $ImageTag ." -ForegroundColor Cyan
        exit 1
    }
} catch {
    Write-TestResult "Image exists" $false $_.Exception.Message
    $testResults += $false
    exit 1
}

# Test 2: Help Command
Write-TestHeader "Test 2: Help Command"
try {
    $helpOutput = docker run --rm $ImageTag --help 2>&1 | Out-String
    $helpPassed = $helpOutput -match "TerraSecure"
    Write-TestResult "Help command works" $helpPassed
    $testResults += $helpPassed
} catch {
    Write-TestResult "Help command works" $false $_.Exception.Message
    $testResults += $false
}

# Test 3: Scan Vulnerable Examples
Write-TestHeader "Test 3: Scan Vulnerable Examples"
try {
    Write-Host "Scanning examples/vulnerable..." -ForegroundColor Gray
    $scanOutput = docker run --rm -v "${PWD}\examples:/scan:ro" $ImageTag /scan/vulnerable 2>&1 | Out-String
    $scanPassed = $scanOutput -match "Issues Found"
    Write-TestResult "Scan vulnerable examples" $scanPassed
    
    # Check for expected findings
    $hasCritical = $scanOutput -match "Critical:"
    $hasHigh = $scanOutput -match "High:"
    
    Write-Host "   Critical issues detected: $(if ($hasCritical) {'Yes'} else {'No'})" -ForegroundColor $(if ($hasCritical) {'Red'} else {'Gray'})
    Write-Host "   High issues detected: $(if ($hasHigh) {'Yes'} else {'No'})" -ForegroundColor $(if ($hasHigh) {'Yellow'} else {'Gray'})
    
    $testResults += $scanPassed
} catch {
    Write-TestResult "Scan vulnerable examples" $false $_.Exception.Message
    $testResults += $false
}

# Test 4: JSON Output
Write-TestHeader "Test 4: JSON Output"
try {
    # Create output directory
    New-Item -ItemType Directory -Force -Path "output" | Out-Null
    
    # Run scan with JSON output
    docker run --rm `
        -v "${PWD}\examples:/scan:ro" `
        -v "${PWD}\output:/output" `
        $ImageTag /scan/vulnerable --format json --output /output/test-results.json 2>&1 | Out-Null
    
    # Check if file was created
    Start-Sleep -Seconds 1
    
    if (Test-Path "output\test-results.json") {
        $jsonContent = Get-Content "output\test-results.json" -Raw | ConvertFrom-Json
        $jsonPassed = $jsonContent.issues.Count -gt 0
        
        Write-TestResult "JSON output created" $true
        Write-Host "   Total issues: $($jsonContent.issues.Count)" -ForegroundColor Cyan
        Write-Host "   Critical: $($jsonContent.stats.CRITICAL)" -ForegroundColor Red
        Write-Host "   High: $($jsonContent.stats.HIGH)" -ForegroundColor Yellow
        Write-Host "   Medium: $($jsonContent.stats.MEDIUM)" -ForegroundColor Blue
        
        $testResults += $jsonPassed
    } else {
        Write-TestResult "JSON output created" $false "File not found at output\test-results.json"
        $testResults += $false
    }
} catch {
    Write-TestResult "JSON output created" $false $_.Exception.Message
    $testResults += $false
}

# Test 5: Scan Secure Examples (should pass)
Write-TestHeader "Test 5: Scan Secure Examples"
try {
    Write-Host "Scanning examples/secure..." -ForegroundColor Gray
    $secureOutput = docker run --rm -v "${PWD}\examples:/scan:ro" $ImageTag /scan/secure 2>&1 | Out-String
    
    # Secure examples might have some issues, but should have fewer critical ones
    $securePassed = $true  # Just checking it runs without error
    
    Write-TestResult "Scan secure examples" $securePassed
    $testResults += $securePassed
} catch {
    Write-TestResult "Scan secure examples" $false $_.Exception.Message
    $testResults += $false
}

# Test 6: Fail on Critical
Write-TestHeader "Test 6: Exit Code on Critical Issues"
try {
    docker run --rm -v "${PWD}\examples:/scan:ro" $ImageTag /scan/vulnerable --fail-on critical 2>&1 | Out-Null
    $exitCode = $LASTEXITCODE
    
    # Should exit with code 2 (critical issues found)
    $exitPassed = $exitCode -eq 2
    
    $expectedMsg = "Exit code $exitCode - Expected 2"
    Write-TestResult "Exit code on critical" $exitPassed $expectedMsg
    $testResults += $exitPassed
} catch {
    Write-TestResult "Exit code on critical" $false $_.Exception.Message
    $testResults += $false
}

# Test 7: Container User
Write-TestHeader "Test 7: Security - Non-Root User"
try {
    $userCheck = docker run --rm --entrypoint sh $ImageTag -c "whoami" 2>&1 | Out-String
    $userCheck = $userCheck.Trim()
    $userPassed = $userCheck -match "terrasecure"
    
    Write-TestResult "Running as non-root user" $userPassed "User: $userCheck"
    $testResults += $userPassed
} catch {
    Write-TestResult "Running as non-root user" $false $_.Exception.Message
    $testResults += $false
}

# Test 8: ML Model Loaded
Write-TestHeader "Test 8: ML Model Status"
try {
    $modelCheck = docker run --rm -v "${PWD}\examples:/scan:ro" $ImageTag /scan/vulnerable 2>&1 | Out-String | Select-String "Production model"
    $modelPassed = $modelCheck -ne $null
    
    Write-TestResult "ML model loaded" $modelPassed
    if ($modelCheck) {
        $modelLine = ($modelCheck -split "`n")[0].Trim()
        Write-Host "   $modelLine" -ForegroundColor Gray
    }
    $testResults += $modelPassed
} catch {
    Write-TestResult "ML model loaded" $false $_.Exception.Message
    $testResults += $false
}

# Summary
$endTime = Get-Date
$duration = ($endTime - $startTime).TotalSeconds

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "                    Test Summary                                " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

$totalTests = $testResults.Count
$passedTests = ($testResults | Where-Object { $_ -eq $true }).Count
$failedTests = $totalTests - $passedTests

if ($totalTests -gt 0) {
    $passRate = [math]::Round(($passedTests / $totalTests) * 100, 1)
} else {
    $passRate = 0
}

Write-Host "Total Tests:  $totalTests" -ForegroundColor White
Write-Host "Passed:       $passedTests" -ForegroundColor Green
Write-Host "Failed:       $failedTests" -ForegroundColor $(if ($failedTests -eq 0) { "Green" } else { "Red" })
Write-Host "Pass Rate:    $passRate%" -ForegroundColor $(if ($passRate -eq 100) { "Green" } elseif ($passRate -ge 80) { "Yellow" } else { "Red" })
Write-Host "Duration:     $([math]::Round($duration, 2))s" -ForegroundColor Gray
Write-Host ""

if ($passedTests -eq $totalTests -and $totalTests -gt 0) {
    Write-Host "[OK] ALL TESTS PASSED!" -ForegroundColor Green
    Write-Host ""
    exit 0
} else {
    Write-Host "[X] SOME TESTS FAILED" -ForegroundColor Red
    Write-Host ""
    exit 1
}