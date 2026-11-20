# DevOps Practical – Flask Application

This repository demonstrates six DevOps practical phases: application development, GitHub Actions CI, Docker containerization, Kubernetes deployment, Kubernetes self-healing, and continuous deployment with Render.

## Project structure

```text
devops-practical/
├── .github/workflows/ci.yml
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
├── .dockerignore
├── .gitignore
├── Dockerfile
├── app.py
├── requirements.txt
├── test_app.py
├── render.yaml
└── README.md
```

## Phase 1 – Flask application

- `/` returns application status and version as JSON.
- `/health` returns a health-check response.
- Dependencies are listed in `requirements.txt`.
- Automated tests are in `test_app.py`.

## Phase 2 – GitHub Actions CI

The workflow at `.github/workflows/ci.yml` runs on pushes and pull requests to `main`. It installs Python 3.11 dependencies, runs pytest, and builds the Docker image.

## Phase 3 – Docker

The `Dockerfile` packages the Flask app using Python 3.11 and Gunicorn.

To publish to Docker Hub:
1. Create a Docker Hub repository named `devops-practical` under account `kgysandeepa`.
2. In GitHub repository Settings → Secrets and variables → Actions, add secrets `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN`.
3. Add repository variable `DOCKERHUB_ENABLED` with value `true`.

The publish job is intentionally skipped until that variable is enabled, so the CI test/build workflow can pass without Docker Hub credentials. Never commit passwords or tokens.

## Phase 4 – Kubernetes deployment

The manifests in `k8s/` deploy two replicas and expose the application with a NodePort Service.

Prerequisites: Docker Desktop, kubectl, and Minikube. The image must first be published to Docker Hub.

```bash
minikube start --driver=docker
kubectl get nodes
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl rollout status deployment/devops-practical
kubectl get pods
kubectl get services
minikube service devops-practical-service
```

## Phase 5 – Kubernetes self-healing

List the application Pods:

```bash
kubectl get pods -l app=devops-practical
```

Delete one Pod, replacing `POD_NAME` with its actual name:

```bash
kubectl delete pod POD_NAME
kubectl get pods -l app=devops-practical -w
```

The Deployment controller should create a replacement Pod and restore the desired replica count to two. Stop watching with Ctrl+C.

## Phase 6 – Continuous deployment with Render

The root-level `render.yaml` defines a Render web service. In Render, create a Blueprint and connect this GitHub repository. Render reads the configuration, builds the Flask application, and can automatically deploy updates from `main`.

After deployment, verify:
- `/` returns the application status JSON.
- `/health` returns `{"status":"healthy"}`.

## Run locally (optional)

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
pip install -r requirements.txt
pytest -v
python app.py
```

Open `http://localhost:5000`.

## Deployment notes

The source code and deployment configuration are committed here. Docker Hub publishing requires the repository and GitHub Actions secrets/variable described above. Kubernetes execution requires a running cluster and a published image. Render deployment requires connecting this repository to a Render account.
