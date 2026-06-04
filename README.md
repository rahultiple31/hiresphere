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

## ArgoCD Deploy

Use ArgoCD to deploy the Helm chart from this repository:

- Chart path: `charts/hiresphere`
- Image repository: `rahultipledocker/hiresphere`
- Image tag: `1.0` by default; the workflow also publishes `latest`, branch tags, and `sha-<short-sha>` tags

The chart deploys a `NodePort` service by default. To see the assigned port:

```bash
kubectl get svc hiresphere -n hiresphere
```

If you prefer a fixed port, set `service.nodePort` to a valid port in the `30000-32767` range, for example `30080`.

## GitHub Actions CI/CD

The workflow lives at `.github/workflows/ci-cd.yml` and runs on pushes to `main` or `master`, pull requests, and manual dispatch.

It performs:

- Static app file validation
- Helm lint and template smoke test
- Docker image build and container health smoke test
- Push to GitHub Container Registry as `ghcr.io/<owner>/hiresphere`
- Push to Docker Hub as `rahultipledocker/hiresphere`
- No Kubernetes deployment stage. ArgoCD should deploy this Helm chart.

Optional repository variables:

- `KUBE_NAMESPACE`: defaults to `hiresphere`
- `HELM_RELEASE_NAME`: defaults to `hiresphere`

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
