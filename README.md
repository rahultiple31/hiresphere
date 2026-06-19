# HireSphere micro-frontends

HireSphere is split into a persistent navigation shell and eight independently editable static services.

## Service map

| Sidebar item | Source folder | Gateway route | Container image |
| --- | --- | --- | --- |
| Workspace | `services/workspace` | `/workspace/` | `hiresphere-workspace` |
| Jobs | `services/jobs` | `/jobs/` | `hiresphere-jobs` |
| Projects | `services/projects` | `/projects/` | `hiresphere-projects` |
| Network | `services/network` | `/network/` | `hiresphere-network` |
| Interview | `services/interview` | `/interview/` | `hiresphere-interview` |
| Profile | `services/profile` | `/profile/` | `hiresphere-profile` |
| HR Studio | `services/hr-studio` | `/hr-studio/` | `hiresphere-hr-studio` |
| Scale | `services/scale` | `/scale/` | `hiresphere-scale` |

The navigation UI lives in `gateway/`. Shared design tokens and safe DOM helpers live in `services/shared/`.

## Edit one service

Each service owns four small files:

- `index.html` — page structure
- `styles.css` — service-specific appearance
- `app.js` — service-specific behavior and data
- `Dockerfile` — independent container image definition

Editing one folder does not require changing the other seven. Shared styling changes belong in `services/shared/base.css`; shell/sidebar changes belong in `gateway/`.

## Run the complete platform

Docker Compose starts the gateway and all eight services:

```bash
docker compose up --build
```

Open `http://localhost:8080`. Stop everything with:

```bash
docker compose down
```

Only the gateway publishes a host port. Internal services communicate on the private `hiresphere` Docker network.

## Kubernetes / ArgoCD

The Helm chart in `charts/hiresphere` deploys nine Deployments: one gateway and eight services. The gateway Service retains the public `NodePort`; internal services use `ClusterIP`.

CI publishes nine separate repositories: `hiresphere-gateway` plus one `hiresphere-<service>` repository for every microservice. Each receives `1.0`, `latest`, and immutable `sha-*` tags.

### Manual CI/CD selector

Open **Actions → HireSphere CI/CD → Run workflow** and choose a component:

- `all` builds and integration-tests the complete platform, then publishes the gateway and all eight services.
- `gateway` integration-tests the complete platform, then publishes only the gateway image.
- Selecting one service, such as `jobs`, smoke-tests and publishes only that service image.

Pushes to `main` or `master` use the `all` flow automatically. Pull requests validate the Helm chart and integration-test the complete platform without publishing images.

## Build one service

```bash
docker build -f services/jobs/Dockerfile -t hiresphere-jobs .
```

Replace `jobs` in the Dockerfile path and image name with any source folder from the table. A service container is intentionally consumed through the gateway because shared assets and same-origin messaging are provided there.

## Architecture

```text
Browser
  -> gateway shell :8080
       -> /workspace/  -> workspace-service:8080
       -> /jobs/       -> jobs-service:8080
       -> /projects/   -> projects-service:8080
       -> /network/    -> network-service:8080
       -> /interview/  -> interview-service:8080
       -> /profile/    -> profile-service:8080
       -> /hr-studio/  -> hr-studio-service:8080
       -> /scale/      -> scale-service:8080
```

## Security notes

User-created content is rendered with DOM text nodes rather than interpolated `innerHTML`. Both gateway and service servers add clickjacking, MIME-sniffing, referrer, and Content Security Policy headers.
