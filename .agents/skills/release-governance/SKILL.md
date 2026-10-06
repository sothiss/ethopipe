---
name: release-governance
description: Enforces a strict 6-step release gate synchronizing version manifests (pyproject.toml, CITATION.cff), lockfiles, documentation, changelog, and git tags.
---

# EthoPipe Release Governance & Packaging Skill

## Role & Primary Mandate
You are the **EthoPipe Release Gatekeeper**. Releasing a scientific Python package requires exact synchronization across version manifests, citations, changelogs, lockfiles, and git tags.

Skipping any of these steps creates version drift, broken citations in academic literature (JOSS/EBAC), and un-reproducible environments.

---

## The 6-Step Non-Negotiable Release Gate

```
[Clean Tree] ──► [Version Bump] ──► [Lockfile Sync] ──► [Changelog & Docs] ──► [Full QA] ──► [Git Tag]
```

### Step 1: Working Tree Cleanliness
Before initiating a release, ensure git state is sterile:
```bash
git status --short
```
Working tree must have zero unstaged or uncommitted changes.

### Step 2: Version Synchronization (SemVer)
Update the version string in all required manifests:
1. `pyproject.toml`:
   ```toml
   [project]
   version = "X.Y.Z"
   ```
2. `CITATION.cff`:
   ```yaml
   version: X.Y.Z
   date-released: YYYY-MM-DD
   ```

### Step 3: Lockfile Synchronization
Re-synchronize and audit dependencies:
```bash
uv lock
uv audit
```

### Step 4: Documentation & Release Notes
1. Create `docs/releases/vX.Y.Z.md` with:
   - Summary of features, fixes, and performance/security optimizations.
   - Grounding references and JOSS citations.
2. Update `CHANGELOG.md` under `## [X.Y.Z] - YYYY-MM-DD`.

### Step 5: Comprehensive QA Gate
Execute the entire 8-step QA pipeline:
```powershell
.\scripts\run_qa.ps1
```
All 8 steps must pass with 0 warnings or failures.

### Step 6: Git Commit & Annotated Tag
Commit the version bump and create an annotated git tag:
```bash
git add pyproject.toml CITATION.cff uv.lock CHANGELOG.md docs/releases/
git commit -m "chore(release): bump version to vX.Y.Z"
git tag -a vX.Y.Z -m "Release vX.Y.Z"
```
