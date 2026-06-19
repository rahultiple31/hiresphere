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

## Local development

Requires Node.js 22+.

```bash
npm ci
npm run dev
```

For the complete production-style platform:

```bash
docker compose up --build
```

Open `http://localhost:8080`.

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

- Docker Compose builds and runs one gateway plus eight micro-frontends.
- The Helm chart deploys the same nine images to Kubernetes.
- `.github/workflows/ci-cd.yml` compiles React, validates Helm, smoke-tests all routes, and publishes selected images.
- `.github/workflows/static.yml` builds `dist/` and deploys it to GitHub Pages.

Only the gateway publishes a host port. Internal containers communicate through the private `hiresphere` network.
