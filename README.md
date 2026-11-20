# DevOps Practical – Flask Application

This project contains the source files for the six phases in the supplied DevOps practical: local development and Git, GitHub Actions CI, Docker, Kubernetes, the Kubernetes self-healing demonstration, and Render deployment.

## Project structure

```text
devops-practical/
├── .github/
│   └── workflows/
│       └── ci.yml
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
├── .dockerignore
├── Dockerfile
├── app.py
├── requirements.txt
├── test_app.py
└── README.md
```

## Before you start

Install Python, Git, Docker Desktop, kubectl and Minikube. Create your own GitHub and Docker Hub accounts. Replace `YOUR_DOCKERHUB_USERNAME` in `k8s/deployment.yaml` with your Docker Hub username before applying the Kubernetes Deployment.

## Phase 1 – Run locally and push to GitHub

Open Command Prompt in this folder and run:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pytest
python app.py
```

Open http://localhost:5000. Stop the server with Ctrl+C.

Create an empty GitHub repository named `devops-practical`, then run (replace the URL with your own repository URL):

```bash
git init
git add .
git commit -m "Initial commit: Flask app and tests"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/devops-practical.git
git push -u origin main
```

If Git asks who you are, configure your commit identity:

```bash
git config --global user.name "Your Name"
git config --global user.email "YOUR_EMAIL_ADDRESS"
```

## Phase 2 – GitHub Actions CI

The workflow is at `.github/workflows/ci.yml`. Push it to the `main` branch. In GitHub, open the repository's **Actions** tab and check that **CI Pipeline** completes successfully.

## Phase 3 – Docker

Start Docker Desktop and wait until it reports that the engine is running. From the project root:

```bash
docker build -t flask-app:v1 .
docker run --rm -p 5000:5000 flask-app:v1
```

Open http://localhost:5000 and stop the container with Ctrl+C.

Log in to Docker Hub, tag and push the image (replace the username):

```bash
docker login
docker tag flask-app:v1 YOUR_DOCKERHUB_USERNAME/flask-app:v1
docker push YOUR_DOCKERHUB_USERNAME/flask-app:v1
```

## Phase 4 – Kubernetes with Minikube

Start Docker Desktop first, then:

```bash
minikube start --driver=docker
kubectl version --client
minikube version
```

Edit `k8s/deployment.yaml` and replace `YOUR_DOCKERHUB_USERNAME` with your Docker Hub username. From the project root apply both manifests:

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl get pods -w
```

Wait until both Pods show `Running`, then press Ctrl+C and check:

```bash
kubectl get pods
kubectl get services
minikube service flask-service
```

## Phase 5 – Kubernetes self-healing demonstration

Get a Pod name and delete one Pod:

```bash
kubectl get pods
kubectl delete pod POD_NAME_FROM_PREVIOUS_COMMAND
kubectl get pods -w
```

Kubernetes should create a replacement Pod to return to the Deployment's desired replica count of two. Capture your own terminal evidence for the practical demonstration.

## Phase 6 – Render deployment

The application reads the `PORT` environment variable supplied by Render and defaults to port 5000 locally. Push the latest code to GitHub, then in Render create a **Web Service** connected to your repository. Select the `main` branch and Docker runtime (the Dockerfile is in the project root). Choose an available plan and region shown in your Render account. Wait for the deployment to become Live and test the generated public URL.

To demonstrate a later change, edit the response string in `app.py`, update the matching expected text in `test_app.py`, then commit and push. Confirm the GitHub Actions workflow passes and Render deploys the new version.

## Important notes

- Replace all uppercase placeholders such as `YOUR_GITHUB_USERNAME`, `YOUR_EMAIL_ADDRESS`, and `YOUR_DOCKERHUB_USERNAME` with your own details. Never share passwords or access tokens in this project.
- The supplied practical uses pinned Flask/Pytest versions and Python 3.9 in CI and Docker to match its instructions.
- These are prepared project files, not proof that the commands have been run. Run each phase on your laptop and take your own screenshots of successful tests, GitHub Actions, Docker, Kubernetes, and Render for any evidence your lecturer requires.
- Render's free-plan availability and terms can change; select only a plan currently offered in your account.
