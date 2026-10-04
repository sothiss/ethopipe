---
name: Feature Idea & RFC
about: Propose an idea or feature through the 5-Gate Step-Gated Pipeline
title: "[IDEA] "
labels: enhancement, gate:idea
---

## 🎯 Problem Statement
<!-- What problem does this solve? What is the user or scientific goal? -->

## 🧭 Track
- [ ] ⚡ `track:bolt` (Performance / Algorithmic Optimization)
- [ ] 🛡️ `track:sentinel` (Security / Input Hardening / Boundaries)
- [ ] 📦 `track:feature` (Schema / Darwin Core / Data Parsing)
- [ ] 🔧 `track:refactor` (Code Simplification / Modularization)

## 🛑 Step-Gated Pre-Flight Check (Do Not Skip Steps!)
- [ ] **Solo Maintainer Filter**: Can this be implemented in pure Python (no Node/npm, Rust, Go) without adding new dependencies?
- [ ] **Target Files**: Enumerate the specific files to be created or modified.
- [ ] **Domain Boundaries**: Canine heart rate bounds [30, 250] BPM, Darwin Core schemas, and linguistic neutrality respected.
- [ ] **Test Strategy**: What test case or Hypothesis boundary test will prove this works?
