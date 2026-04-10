<#
.SYNOPSIS
    SHADOWSCAN PRO - PowerShell Launcher
.DESCRIPTION
    Advanced Offensive Security Framework
    Developed by ROHAIB TECHNICAL | +92 306 3844400
#>

Write-Host @"
============================================================
   SHADOWSCAN PRO - Offensive Security Framework
   Developed by ROHAIB TECHNICAL | +92 306 3844400
============================================================
"@ -ForegroundColor Red

# Activate virtual environment if exists
if (Test-Path ".\venv\Scripts\Activate.ps1") {
    . .\venv\Scripts\Activate.ps1
}

# Run ShadowScan
python -m shadowscan $args