$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $RepoRoot

python scripts/build_figures.py
python -m py_compile scripts/build_figures.py

pdflatex -interaction=nonstopmode -halt-on-error main.tex
biber main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex

New-Item -ItemType Directory -Force output | Out-Null
Copy-Item -Force main.pdf output/fast_mc_zdc_manuscript.pdf

$LogProblems = Select-String -Path main.log -Pattern "LaTeX Warning|Undefined control sequence|Overfull|Underfull" -SimpleMatch:$false
if ($LogProblems) {
    $LogProblems | ForEach-Object { Write-Error $_.Line }
}

$PdfText = Join-Path $env:TEMP "fast_mc_zdc_manuscript.txt"
pdftotext output/fast_mc_zdc_manuscript.pdf $PdfText
$TextProblems = Select-String -Path $PdfText -Pattern "\?\?|0\.4636|undefined references" -SimpleMatch:$false
if ($TextProblems) {
    $TextProblems | ForEach-Object { Write-Error $_.Line }
}

Write-Host "Built output/fast_mc_zdc_manuscript.pdf"
