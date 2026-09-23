param([string]$Python = "python")

$ErrorActionPreference = "Stop"

function Invoke-Checked {
    param([string]$Program, [string[]]$Arguments)
    & $Program @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "$Program failed with exit code $LASTEXITCODE"
    }
}

$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $RepoRoot

Invoke-Checked $Python @("scripts/build_figures.py")
Invoke-Checked $Python @("-m", "py_compile", "scripts/build_figures.py")

Invoke-Checked "pdflatex" @("-interaction=nonstopmode", "-halt-on-error", "main.tex")
Invoke-Checked "biber" @("main")
Invoke-Checked "pdflatex" @("-interaction=nonstopmode", "-halt-on-error", "main.tex")
Invoke-Checked "pdflatex" @("-interaction=nonstopmode", "-halt-on-error", "main.tex")

$LogProblems = Select-String -Path main.log -Pattern "LaTeX Warning|Undefined control sequence|Overfull|Underfull" -SimpleMatch:$false
if ($LogProblems) {
    $LogProblems | ForEach-Object { Write-Error $_.Line }
}

New-Item -ItemType Directory -Force audit/qa_runs/build | Out-Null
$PdfText = Join-Path $RepoRoot "audit/qa_runs/build/manuscript.txt"
Invoke-Checked "pdftotext" @("main.pdf", $PdfText)
$TextProblems = Select-String -Path $PdfText -Pattern "\?\?|0\.7785|0\.9330|validation-only evidence|undefined references" -SimpleMatch:$false
if ($TextProblems) {
    $TextProblems | ForEach-Object { Write-Error $_.Line }
}

New-Item -ItemType Directory -Force output | Out-Null
Copy-Item -LiteralPath main.pdf -Destination output/fast_mc_zdc_manuscript.pdf -Force
Write-Host "Built output/fast_mc_zdc_manuscript.pdf"
