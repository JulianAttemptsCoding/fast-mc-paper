#!/usr/bin/env bash
# Build the proposed revision in this folder only. Does not touch ../../main.tex or ../../output.
set -e
cd "$(dirname "$0")"
python build_proposal_figures.py
pdflatex -interaction=nonstopmode -halt-on-error main.tex > build.log 2>&1
biber main > biber.log 2>&1
pdflatex -interaction=nonstopmode -halt-on-error main.tex > build.log 2>&1
pdflatex -interaction=nonstopmode -halt-on-error main.tex > build.log 2>&1
grep -E "LaTeX Warning|Undefined control|Overfull|Underfull|^!" main.log || echo "no LaTeX warnings"
grep -E "Output written" main.log
pdftotext -layout main.pdf main.txt
grep -n -E "\?\?" main.txt || echo "no unresolved references"
