# phase3_scaling_notes.md

## Phase 3: Scaling with multiple workers & Traefik

What we did:
- Increased Celery workers concurrency: --concurrency=8
- Scaled API service to 16 replicas in docker-compose
- Used Traefik as reverse proxy / load balancer on port 80

Commands we ran:
# Start Redis
docker run -d -p 6379:6379 --name redis redis

# Start many Celery workers
celery -A phase2_queue_safe_api multi start worker1 worker2 worker3 -c 8 --loglevel=info

# Or in docker-compose (simplified example)
services:
  api:
    build: .
    deploy:
      replicas: 16
  traefik:
    image: traefik:v2.10
    command: --providers.docker --entrypoints.web.address=:80
    ports:
      - "80:80"
