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

For a Kubernetes deployment, use the Helm chart directly instead of Docker Compose:

```bash
helm upgrade --install hiresphere charts/hiresphere \
  --namespace hiresphere \
  --create-namespace
```

If you still want a quick local containerized smoke test, Docker Compose may be used only for debugging; the actual application deployment flow for this repo is Kubernetes + Helm.

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
- The Helm chart is the production deployment path for all microservices on Kubernetes.
- `.github/workflows/ci-cd.yml` compiles React, validates Helm manifests, and publishes selected images.
- `.github/workflows/static.yml` builds `dist/` and deploys it to GitHub Pages.

Only the gateway publishes a host port. Internal containers communicate through the private `hiresphere` network.

Install the application and database layer:

```bash
helm upgrade --install hiresphere charts/hiresphere \
  --namespace hiresphere \
  --create-namespace
```

For production, provide a pre-created Secret instead of chart-managed credentials. It must contain `postgres-database`, `postgres-username`, `postgres-password`, `mongodb-database`, `mongodb-root-username`, and `mongodb-root-password`:

```bash
helm upgrade --install hiresphere charts/hiresphere \
  --namespace hiresphere \
  --create-namespace \
  --set database.auth.existingSecret=hiresphere-database-credentials
```

Check the unified database workload:

```bash
kubectl get statefulset,pod,pvc,service \
  -n hiresphere \
  -l app.kubernetes.io/component=database
```
