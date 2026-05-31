---
title: 'EthoPipe: A Python-based ETL Pipeline for Standardizing Applied Canine Ethology and Physiological Telemetry'
tags:
  - Python
  - canine behavior
  - ethology
  - ETL
  - Darwin Core
  - veterinary science
authors:
  - name: Alice Severi Gonçalves
    orcid: 0009-0003-0048-8982
    affiliation: 1
affiliations:
  - name: Independent Researcher
    index: 1
date: 31 May 2026
bibliography: paper.bib
---

# Summary

**EthoPipe** is a Python-based Extract, Transform, Load (ETL) pipeline engineered to resolve the data fragmentation bottleneck in applied canine ethology and behavioral clinical studies. By formalizing strict, veterinary-validated boundary constraints and mapping categorical motor patterns to international data sharing standards, EthoPipe provides a reliable engineering bridge between raw veterinary narratives and standardized, open-science databases.

# Statement of Need

Canine behavioral research and veterinary clinical tracking are heavily plagued by fragmented, heterogeneous data collection methods. Primary physiological metrics (such as heart rate, respiratory rate, and body temperature) and behavioral observations (such as ethogram frequency counts) are typically recorded via manual unstructured narratives, varying spreadsheet formats, or disparate sensor logs. This fragmentation severely restricts cross-study data aggregation, limits meta-analytic potential, and hinders reproducibility across institutions.

**EthoPipe** addresses these challenges by introducing:
* **Deterministic Runtime Type Validation**: Built on Pydantic v2 to enforce rigorous, veterinary-validated boundaries on all incoming fields (e.g., restricting respiratory rates strictly to resting or active canine ranges).
* **International Standards Alignment**: Automatically mapping validated ethological observations to Darwin Core (DwC) terms [@darwin2012] such as `dwc:individualID`, `dwc:eventDate`, and `dwc:basisOfRecord` (`HumanObservation` versus `MachineObservation`).
* **Robust Behavioral Categorization**: Structuring motor patterns and displacement cues strictly against a standardized canine behavioral controlled vocabulary.

# Implementation and Architecture

EthoPipe is designed as a modular, lightweight Python package consisting of four core modules:
1. **Extraction (`extraction.py`)**: Uses stateful regular expression models to parse clinical narrative reports, dynamically extracting both physiological vitals (e.g., heart rate in BPM, temperature in °C) and ethogram-aligned behaviors (e.g., barks, lip licking, yawning) along with their frequency counts.
2. **Data Models (`models.py`)**: Defines strict `EthologicalObservation` schemas. This layer implements multi-field custom validators—such as size-dependent heart rate ranges (e.g., small versus giant breeds) and automatic ontology URI lookups mapped to the Gene Ontology (GO) and Neuro Behavior Ontology (NBO).
3. **Ingestion (`ingestion.py`)**: Supports batch ingestion of both CSV and JSON formats, applying custom column mapping and isolating invalid records into structured quarantine outputs.
4. **Loading (`loader.py` & `api.py`)**: Connects validated observations to target databases (such as Google Cloud Firestore) while exposing lightweight FastAPI endpoints for validation and data submission.

# References
