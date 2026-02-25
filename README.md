# plate-ocr-load-testing-case-study
High-level architecture & load testing write-up for a scalable ANPR system (NDA-protected project)

# Scalable ANPR System (Automatic Number Plate Recognition)

# Scalable ANPR Infrastructure & Load Testing (2025 Project)

**Status**: Proof-of-Concept & Architecture Design  
**Role**: Backend/DevOps Engineer (freelance/contract)  
**Timeline**: 2025  
**Confidentiality Note**: This is a high-level technical write-up of work performed under NDA. No proprietary code, data, or company-specific details are included.

## Project Overview
Designed and stress-tested a scalable backend infrastructure for an Automatic Number Plate Recognition (ANPR) system with OCR capabilities.

Main responsibilities & achievements:
- Built and load-tested an API layer for plate image processing
- Implemented zero-data-loss message processing pipeline
- Scaled horizontally to handle high concurrency
- Simulated production-like conditions in a VM environment

## Key Technologies & Stack
- Virtualization: Proxmox VE
- OS: Ubuntu Server
- Containerization: Docker + docker-compose
- Orchestration / Proxy: Traefik
- Queue & Task Processing: Redis + Celery (with unlimited retries)
- Database: PostgreSQL (with replication considerations)
- Alternative explored: ClickHouse, TimescaleDB, Kafka (KRaft mode)
- Load Testing: k6
- Fallback: CPU-only OCR processing

## Architecture Highlights
Microservice-oriented design with clear separation of concerns:

- **Frontend/API requests** → Traefik → API containers
- **Heavy tasks** (OCR, processing) → Celery workers + Redis queue
- **Storage** → PostgreSQL / potential time-series DB
- **Offline/air-gapped support** → Docker .tar images for deployment without internet

Designed for:
- Horizontal scaling (tested up to 16 replicas × 8 workers)
- Zero data loss (unlimited retries + queue persistence)
- High throughput under stress

## Load Testing Results (Highlights)
Ran extensive k6 scenarios simulating real-world traffic:

| Scenario              | Virtual Users | RPS   | Success Rate | Failure Rate | Data Loss |
|-----------------------|---------------|-------|--------------|--------------|-----------|
| Baseline              | 100           | ~25   | 99.9%        | 0.1%         | 0%        |
| Peak load             | 700           | ~69   | 99.87–99.96% | 0.04–0.64%   | 0%        |

Achieved production-ready stability with zero permanent data loss even under failure injection.

## Challenges & Solutions
- Docker image access in restricted networks → .tar export/import workflow
- GPU unavailability → reliable CPU fallback
- Multipart upload issues → debugged and stabilized endpoint
- High-concurrency queue overload → tuned Celery + Redis + retry policy

## What I Learned / Skills Demonstrated
- Designing for zero-data-loss in distributed systems
- Load & stress testing large-scale APIs
- Handling offline/air-gapped deployments
- Microservices scaling & observability basics
- Troubleshooting in constrained environments (sanctions, limited resources)

## Future Improvements (planned but not implemented)
- Full Kafka integration (KRaft mode)
- Prometheus + Grafana monitoring
- GPU acceleration for OCR
- Automated client updates in offline mode

