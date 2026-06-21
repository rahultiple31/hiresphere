# HireSphere React micro-frontends

HireSphere is a React 19 talent marketplace composed of a persistent gateway shell and eight independently deployable micro-frontends.

| Micro-frontend | Source route | Container image |
| --- | --- | --- |
| Workspace | `/workspace/` | `hiresphere-workspace` |
| Jobs | `/jobs/` | `hiresphere-jobs` |
| Projects | `/projects/` | `hiresphere-projects` |
| Network | `/network/` | `hiresphere-network` |
| Interview | `/interview/` | `hiresphere-interview` |
| Profile | `/profile/` | `hiresphere-profile` |
| HR Studio | `/hr-studio/` | `hiresphere-hr-studio` |
| Scale | `/scale/` | `hiresphere-scale` |

## React architecture

- `src/gateway-main.jsx` owns navigation, theme, global search, roles, and notifications.
- `src/service-main.jsx` contains the service views and React state-driven interactions.
- `src/bridge.js` provides a small same-origin message bridge between the shell and micro-frontends.
- `vite.config.js` builds every component as an isolated static artifact.
- `services/shared/` contains shared design tokens and responsive layout styles.

The services keep independent Docker images and Kubernetes Deployments. React is compiled during the image build; production containers serve only optimized static assets through unprivileged Nginx.

## Data storage

The Helm chart includes one database StatefulSet pod with two purpose-specific containers:

- PostgreSQL stores transactional SQL records: accounts, candidate profiles, skills, jobs, applications, projects, milestones, interviews, and payments.
- MongoDB stores flexible NoSQL documents: feed posts, notifications, activity events, and search documents.
- One internal Kubernetes Service exposes PostgreSQL on `5432` and MongoDB on `27017`.
- Separate persistent volume claims protect PostgreSQL and MongoDB data across pod restarts.
- Initialization scripts create relational constraints, indexes, MongoDB validators, and document indexes on the first startup.
- Credentials are generated on the first Helm install and retained on upgrades. Production clusters can instead reference an externally managed Secret.

The current frontend containers serve static React assets and do not connect directly to either database. Backend/API services should consume these internal endpoints and credentials; database credentials must never be sent to browser code.

## Local development

Requires Node.js 22+.

```bash
npm ci
npm run dev
```

For a Kubernetes deployment, use the per-service Helm charts directly instead of Docker Compose. The exact install flow is:

```bash
helm upgrade --install api charts/api \
  --namespace hiresphere-api \
  --create-namespace

helm upgrade --install gateway charts/gateway \
  --namespace hiresphere-gateway \
  --create-namespace

helm upgrade --install workspace charts/workspace \
  --namespace hiresphere-workspace \
  --create-namespace

helm upgrade --install jobs charts/jobs \
  --namespace hiresphere-jobs \
  --create-namespace

helm upgrade --install projects charts/projects \
  --namespace hiresphere-projects \
  --create-namespace

helm upgrade --install network charts/network \
  --namespace hiresphere-network \
  --create-namespace

helm upgrade --install interview charts/interview \
  --namespace hiresphere-interview \
  --create-namespace

helm upgrade --install profile charts/profile \
  --namespace hiresphere-profile \
  --create-namespace

helm upgrade --install hr-studio charts/hr-studio \
  --namespace hiresphere-hr-studio \
  --create-namespace

helm upgrade --install scale charts/scale \
  --namespace hiresphere-scale \
  --create-namespace
```

For GitOps-based delivery, apply the bootstrap manifest and one Argo CD Application per service:

```bash
kubectl apply -f argocd-bootstrap.yaml
kubectl apply -f argocd-applications/
```

If you still want a quick local containerized smoke test, Docker Compose may be used only for debugging; the actual application deployment flow for this repo is Kubernetes + Helm + Argo CD.

## Production builds

Build only the gateway:

```bash
npm run build
```

Build all nine React applications and assemble the GitHub Pages artifact:

```bash
npm run build:pages
```

The assembled static site is written to `dist/`. Individual component artifacts are written to `.build/<component>/`.

## Deployment

- Docker Compose is optional only for local debugging or smoke testing.
- The `charts/hiresphere` platform chart is a required production deployment.
- Each service has its own Helm chart under `charts/` and its own namespace for isolation.
- The repo includes per-service Argo CD application manifests under `argocd-applications/`.
- `.github/workflows/ci-cd.yml` compiles React, validates Helm manifests, and publishes selected images.
- `.github/workflows/static.yml` builds `dist/` and deploys it to GitHub Pages.

Install the gateway, API, and frontend services with the exact per-service namespaces:

```bash
helm upgrade --install hiresphere charts/hiresphere \
  --namespace hiresphere \
  --create-namespace \
  --values charts/hiresphere/values-prod.yaml

helm upgrade --install api charts/api \
  --namespace hiresphere-api \
  --create-namespace

helm upgrade --install gateway charts/gateway \
  --namespace hiresphere-gateway \
  --create-namespace

helm upgrade --install workspace charts/workspace \
  --namespace hiresphere-workspace \
  --create-namespace

helm upgrade --install jobs charts/jobs \
  --namespace hiresphere-jobs \
  --create-namespace

helm upgrade --install projects charts/projects \
  --namespace hiresphere-projects \
  --create-namespace

helm upgrade --install network charts/network \
  --namespace hiresphere-network \
  --create-namespace

helm upgrade --install interview charts/interview \
  --namespace hiresphere-interview \
  --create-namespace

helm upgrade --install profile charts/profile \
  --namespace hiresphere-profile \
  --create-namespace

helm upgrade --install hr-studio charts/hr-studio \
  --namespace hiresphere-hr-studio \
  --create-namespace

helm upgrade --install scale charts/scale \
  --namespace hiresphere-scale \
  --create-namespace
```

Apply the GitOps bootstrap and all required application definitions, including
the mandatory `hiresphere` platform application:

```bash
kubectl apply -f argocd-bootstrap.yaml
kubectl apply -f argocd-applications/
```

The manifests use the public HTTPS repository URL
`https://github.com/rahultiple31/hiresphere.git`. Use that exact URL in the
Argo CD UI or CLI. Do not use `git@github.com:rahultiple31/hiresphere.git`
unless an SSH deploy key has first been registered in Argo CD.

For production, each service can still use explicit values overrides and image pull secrets. The Argo CD project allows the platform to sync each chart into its own namespace independently.
