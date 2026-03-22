# Integration Guide

## What This File Is For
Use this guide to install AlphaPatch into **another repository** (your project repo).

## Install In Your Repo (Fast Path)
1. Add AlphaPatch to your repo (copy this repo or add it as a subfolder).
2. Run `scripts/install.sh` to copy the workflow template into your repo:
   - It will create `.github/workflows/alphapatch.yml`.
3. Add required secrets (see below).
4. Open a new issue to trigger AlphaPatch.

## Install In Your Repo (Manual)
1. Copy `.github/templates/alphapatch.yml` to `.github/workflows/alphapatch.yml`.
2. Adjust the environment variables in the workflow.
3. Add required secrets (see below).
4. Open a new issue to trigger AlphaPatch.

## Required GitHub Settings

To allow AlphaPatch to create draft PRs, ensure the repository Actions settings allow write access:
1. Repository Settings → Actions → General → Workflow permissions → **Read and write permissions**.
2. Enable **Allow GitHub Actions to create and approve pull requests**.

## Required Secrets

Set these repository secrets:
- `GEMINI_API_KEY` (e.g. `AIzaSy...`) for Gemini API access.
- `GEMINI_MODEL` (e.g. `gemini-2.5-flash`)

We used Gemini as our primary LLM provider, but AlphaPatch is designed to be provider-agnostic.
If you use a different provider, set the corresponding secrets and update the workflow env.

## Optional Configuration
- `ENABLE_DRAFT_PR` (default `1`)
- `ENABLE_LABELS` (default `0`)
- `TEST_COMMAND` (e.g. `pytest -q`)
- `TEST_TIMEOUT` (seconds, default `600`)

## Verify
1. Open a new issue with a clear change request.
2. Watch the Actions log and check for an AlphaPatch comment.
3. If `ENABLE_DRAFT_PR=1`, confirm a draft PR was created.
