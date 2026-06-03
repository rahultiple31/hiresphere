# HireSphere

HireSphere is a static, browser-ready product prototype for a heavy-scale hiring, freelancing, mock-interview, and professional networking ecosystem.

## Run

Open `index.html` in a browser. No Node.js, npm, backend, or dev server is required.

## Docker

Build and run locally:

```bash
docker build -t hiresphere:local .
docker run --rm -p 8080:8080 hiresphere:local
```

Open `http://localhost:8080`.

## Helm Deploy

Deploy to Kubernetes:

```bash
helm upgrade --install hiresphere ./charts/hiresphere \
  --namespace hiresphere \
  --create-namespace \
  --set image.repository=ghcr.io/YOUR_ORG/hiresphere \
  --set image.tag=latest
```

For local access without ingress:

```bash
kubectl port-forward svc/hiresphere 8080:80 -n hiresphere
```

## GitHub Actions CI/CD

The workflow lives at `.github/workflows/ci-cd.yml` and runs on pushes to `main` or `master`, pull requests, and manual dispatch.

It performs:

- Static app file validation
- Helm lint and template smoke test
- Docker image build
- Push to GitHub Container Registry as `ghcr.io/<owner>/hiresphere`
- Kubernetes deployment with `helm upgrade --install`

Required secret for deployment:

- `KUBECONFIG_B64`: base64-encoded kubeconfig for the target cluster

Optional secret for private GitHub Container Registry images:

- `GHCR_PULL_TOKEN`: GitHub token with package read access. When present, the workflow creates a `ghcr-pull-secret` image pull secret in Kubernetes.

Optional repository variables:

- `KUBE_NAMESPACE`: defaults to `hiresphere`
- `HELM_RELEASE_NAME`: defaults to `hiresphere`
- `GHCR_PULL_USERNAME`: defaults to the workflow actor

## Included Modules

- Candidate and freelancer workspace
- Job search with filters, save, apply, recommendations, and tracker
- Project marketplace with filters, bidding, team invite actions, escrow milestones, and invoices
- Professional social feed and referrals
- Real-time interview mockup with 20-minute timer, camera/screen-share UI, chat, recording status, ratings, and STAR feedback
- Candidate profile with resume, cover letter, photo, certificates, portfolio, and self-interview video upload states
- HR studio for job and project creation
- AI candidate matching shortlist panel
- Heavy-scale architecture section for frontend, API gateway, microservices, WebSocket, Kafka, Redis, PostgreSQL, MongoDB, S3/Azure Blob, Kubernetes, Helm, Terraform, and CI/CD

## Generated Asset

The hero image was generated with the built-in image generation tool and copied into `assets/talent-command-center.png` for local project use.
