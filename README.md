# Scalable ANPR Load Testing & Architecture Case Study (2025)

High-level technical write-up and educational demos for a scalable Automatic Number Plate Recognition (ANPR) backend system.

**Status**: Proof-of-Concept & Load-Tested Architecture  
**Role**: Backend / DevOps Engineer (freelance/contract)  
**Timeline**: 2025  
**Confidentiality Note**: This repository contains **no proprietary code, real endpoints, company data, or sensitive logic** due to NDA. All content is generalized, educational, and inspired by real-world work performed in 2025.

## Project Summary

Designed, implemented, and stress-tested a scalable, zero-data-loss backend for image-based plate recognition.

Key achievements:
- Built async API with queue-based processing
- Implemented unlimited retries for zero permanent data loss
- Scaled horizontally with multiple workers and replicas
- Load-tested under extreme concurrency with excellent results

## Key Technologies Used

- **API Framework**: FastAPI (Python)
- **Queue & Async Processing**: Celery + Redis
- **Load Balancing / Proxy**: Traefik
- **Containerization**: Docker + docker-compose
- **Virtualization**: Proxmox VE (VM environment)
- **Load Testing**: k6
- **Fallback / Reliability**: CPU-only processing, unlimited task retries

Explored (but not fully implemented in demos): PostgreSQL replication, Kafka KRaft mode, TimescaleDB, offline .tar deployments.

## Architecture Overview
Client → Traefik (port 80) → API Replicas (FastAPI)
↓
Redis Queue (broker)
↓
Celery Workers (concurrency=8+)
↓
Processing (OCR simulation) → Result


Core features:
- Immediate response with task_id (async)
- Background heavy tasks via Celery
- Unlimited retries (`max_retries=None`) → **zero data loss**
- Horizontal scaling (tested up to 16 replicas × 8 workers)

## Development Phases & Code Demos

The project evolved in clear phases. Each phase has a corresponding file or script in this repo:

### Phase 1 – Basic API Testing (Local Endpoint)
- Simple POST requests to test image upload and JSON response
- Debugged multipart issues and 405 errors
**File**: `phase1_basic_test.py`

### Phase 2 – Queue Safety & Zero Data Loss
- Introduced Redis + Celery
- Unlimited retries for guaranteed delivery
**File**: `phase2_queue_safe_api.py`

### Phase 3 – Horizontal Scaling
- Multiple Celery workers (concurrency=8)
- API replicas + Traefik load balancing
**File**: `phase3_scaling_notes.md` (conceptual notes & commands)

### Phase 4 – Heavy Load Testing (k6)
- Simulated 700 concurrent users
- Measured RPS, failure rate, data integrity
**File**: `phase4_k6_load_test.js`

**Load Test Highlights** (Phase 4 – Peak Results):

| Scenario      | Virtual Users | RPS   | Success Rate   | Failure Rate   | Data Loss |
|---------------|---------------|-------|----------------|----------------|-----------|
| Baseline      | 100           | ~25   | 99.9%          | 0.1%           | 0%        |
| Peak Load     | 700           | ~69   | 99.87–99.96%   | 0.04–0.64%     | **0%**    |

Achieved **production-ready stability** with zero permanent data loss under failure conditions.

## Demo Frontend Interfaces

Two static HTML files to show how clients could interact with the API:

- [demo-text-input.html](./demo-text-input.html)  
  Basic text input → echo response (early testing concept)

- [demo-image-upload.html](./demo-image-upload.html)  
  Image upload with preview → mock processing response

**Note**: These are purely educational. Fetch URLs are placeholders. For local testing, run one of the mock servers and update the URL in JavaScript.

## How to Run the Demos Locally

1. Install dependencies (Python 3.10+)
```
pip install fastapi uvicorn celery redis requests
```

3. Start Redis (required for Celery)
```
docker run -d -p 6379:6379 --name redis redis
```

5. Run Celery worker (for queue processing)
```
#    (run this in a separate terminal)
celery -A phase2_queue_safe_api worker --loglevel=info --concurrency=4
```

4. Run API server
```
#    (run this in another terminal)
uvicorn phase2_queue_safe_api:app --reload
```

5. Open HTML demo files in browser and update fetch URLs
```
#    - Open demo-text-input.html or demo-image-upload.html
#    - Edit the JavaScript fetch() line to point to:
#      http://127.0.0.1:8000/upload/   (or your chosen endpoint)
#    - Refresh the page and test
```

6. Run k6 load test (optional - after API is running)
```
k6 run phase4_k6_load_test.js
```

### Challenges Solved

Multipart upload crashes → fixed with proper handling & python-multipart
GPU unavailability → reliable CPU fallback
High concurrency overload → tuned queue + retry policy
Restricted network (sanctions) → .tar-based offline Docker deployment

### Skills Demonstrated

Designing fault-tolerant async systems
Implementing zero-data-loss pipelines
Horizontal scaling with containers & queues
Load & stress testing (k6)
Working in constrained environments

### Future Work (Planned)

Full Kafka KRaft integration for higher throughput
Monitoring stack (Prometheus + Grafana)
GPU acceleration when hardware available
Offline client update mechanism

This repo serves as a case study of real-world backend scaling work in 2025.
Feel free to reach out for questions or deeper discussions.
