# Container Reliability Lab

A compact, containerized Python service with Kubernetes health probes and a Prometheus metrics endpoint. The project is a reproducible local lab for deployment, basic observability and service reliability concepts.

## What it demonstrates

- A small HTTP service with separate liveness and readiness endpoints.
- Request and process metrics in Prometheus text exposition format.
- A hardened Kubernetes deployment with two replicas, resource requests/limits and health probes.
- Prometheus scrape configuration for the service.

## Run locally

```bash
python app/server.py
```

Visit `http://localhost:8080/`, `http://localhost:8080/healthz`, `http://localhost:8080/readyz` or `http://localhost:8080/metrics`.

## Build and run with Docker

```bash
docker build -t container-reliability-lab:local .
docker run --rm -p 8080:8080 container-reliability-lab:local
```

## Deploy to Kubernetes

Build the image in the cluster's accessible image registry or local image store, then apply the manifests:

```bash
kubectl apply -f kubernetes/
```

The Deployment references `container-reliability-lab:local` and uses `IfNotPresent`; adjust the image name for a remote registry. The Prometheus file is a scrape example and expects a Prometheus instance that can reach the service.
