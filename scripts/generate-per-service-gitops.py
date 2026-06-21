from pathlib import Path
from textwrap import dedent

root = Path(__file__).resolve().parents[1]
repo_url = "https://github.com/rahultiple31/hiresphere.git"
services = [
    ("gateway", "rahultipledocker/hiresphere-gateway", "gateway"),
    ("api", "rahultipledocker/hiresphere-api", "api"),
    ("workspace", "rahultipledocker/hiresphere-workspace", "workspace"),
    ("jobs", "rahultipledocker/hiresphere-jobs", "jobs"),
    ("projects", "rahultipledocker/hiresphere-projects", "projects"),
    ("network", "rahultipledocker/hiresphere-network", "network"),
    ("interview", "rahultipledocker/hiresphere-interview", "interview"),
    ("profile", "rahultipledocker/hiresphere-profile", "profile"),
    ("hr-studio", "rahultipledocker/hiresphere-hr-studio", "hr-studio"),
    ("scale", "rahultipledocker/hiresphere-scale", "scale"),
]

namespace_map = {
    "gateway": "hiresphere-gateway",
    "api": "hiresphere-api",
    "workspace": "hiresphere-workspace",
    "jobs": "hiresphere-jobs",
    "projects": "hiresphere-projects",
    "network": "hiresphere-network",
    "interview": "hiresphere-interview",
    "profile": "hiresphere-profile",
    "hr-studio": "hiresphere-hr-studio",
    "scale": "hiresphere-scale",
}


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(content).lstrip("\n"), encoding="utf-8")


for name, image, chart_name in services:
    chart_dir = root / "charts" / chart_name
    write(
        chart_dir / "Chart.yaml",
        f"""
        apiVersion: v2
        name: {chart_name}
        description: Helm chart for the {name} service
        type: application
        version: 0.1.0
        appVersion: "1.0.0"
        """,
    )
    write(
        chart_dir / "values.yaml",
        f"""
        replicaCount: 1

        image:
          repository: {image}
          tag: "1.0"
          pullPolicy: IfNotPresent

        service:
          type: ClusterIP
          port: 8080
          targetPort: 8080

        ingress:
          enabled: false
          className: ""
          annotations: {{}}
          hosts: []
          tls: []

        resources:
          requests:
            cpu: 50m
            memory: 64Mi
          limits:
            cpu: 250m
            memory: 256Mi

        livenessProbe:
          httpGet:
            path: /healthz
            port: http
          initialDelaySeconds: 10
          periodSeconds: 10

        readinessProbe:
          httpGet:
            path: /healthz
            port: http
          initialDelaySeconds: 5
          periodSeconds: 5
        """,
    )
    write(
        chart_dir / "templates" / "_helpers.tpl",
        f"""
        {{- define "{chart_name}.fullname" -}}
        {name}-service
        {{- end }}

        {{- define "{chart_name}.labels" -}}
        app.kubernetes.io/name: {chart_name}
        app.kubernetes.io/instance: {{ .Release.Name }}
        app.kubernetes.io/component: {name}
        {{- end }}
        """,
    )
    write(
        chart_dir / "templates" / "deployment.yaml",
        f"""
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: {{ include "{chart_name}.fullname" . }}
          namespace: {{ .Release.Namespace | quote }}
          labels:
            {{- include "{chart_name}.labels" . | nindent 8 }}
        spec:
          replicas: {{ .Values.replicaCount }}
          selector:
            matchLabels:
              {{- include "{chart_name}.labels" . | nindent 12 }}
          template:
            metadata:
              labels:
                {{- include "{chart_name}.labels" . | nindent 14 }}
            spec:
              containers:
                - name: {name}
                  image: {{ printf "%s:%s" .Values.image.repository .Values.image.tag | quote }}
                  imagePullPolicy: {{ .Values.image.pullPolicy }}
                  ports:
                    - name: http
                      containerPort: {{ .Values.service.targetPort }}
                  livenessProbe:
                    {{- toYaml .Values.livenessProbe | nindent 20 }}
                  readinessProbe:
                    {{- toYaml .Values.readinessProbe | nindent 20 }}
                  resources:
                    {{- toYaml .Values.resources | nindent 20 }}
        """,
    )
    write(
        chart_dir / "templates" / "service.yaml",
        f"""
        apiVersion: v1
        kind: Service
        metadata:
          name: {{ include "{chart_name}.fullname" . }}
          namespace: {{ .Release.Namespace | quote }}
          labels:
            {{- include "{chart_name}.labels" . | nindent 8 }}
        spec:
          type: {{ .Values.service.type }}
          selector:
            {{- include "{chart_name}.labels" . | nindent 10 }}
          ports:
            - port: {{ .Values.service.port }}
              targetPort: {{ .Values.service.targetPort }}
              protocol: TCP
              name: http
        """,
    )
    write(
        chart_dir / "templates" / "ingress.yaml",
        f"""
        {{- if .Values.ingress.enabled }}
        apiVersion: networking.k8s.io/v1
        kind: Ingress
        metadata:
          name: {{ include "{chart_name}.fullname" . }}
          namespace: {{ .Release.Namespace | quote }}
          labels:
            {{- include "{chart_name}.labels" . | nindent 8 }}
          {{- with .Values.ingress.annotations }}
          annotations:
            {{- toYaml . | nindent 8 }}
          {{- end }}
        spec:
          {{- with .Values.ingress.className }}
          ingressClassName: {{ . }}
          {{- end }}
          {{- with .Values.ingress.tls }}
          tls:
            {{- toYaml . | nindent 8 }}
          {{- end }}
          rules:
            {{- range .Values.ingress.hosts }}
            - host: {{ .host | quote }}
              http:
                paths:
                  {{- range .paths }}
                  - path: {{ .path }}
                    pathType: {{ .pathType }}
                    backend:
                      service:
                        name: {{ include "{chart_name}.fullname" $ }}
                        port:
                          number: {{ $.Values.service.port }}
                  {{- end }}
            {{- end }}
        {{- end }}
        """,
    )

bootstrap = root / "argocd-bootstrap.yaml"
write(
    bootstrap,
    f"""
    apiVersion: v1
    kind: Namespace
    metadata:
      name: argocd
    ---
    apiVersion: v1
    kind: Namespace
    metadata:
      name: hiresphere
    ---
    apiVersion: v1
    kind: Namespace
    metadata:
      name: hiresphere-gateway
    ---
    apiVersion: v1
    kind: Namespace
    metadata:
      name: hiresphere-api
    ---
    apiVersion: v1
    kind: Namespace
    metadata:
      name: hiresphere-workspace
    ---
    apiVersion: v1
    kind: Namespace
    metadata:
      name: hiresphere-jobs
    ---
    apiVersion: v1
    kind: Namespace
    metadata:
      name: hiresphere-projects
    ---
    apiVersion: v1
    kind: Namespace
    metadata:
      name: hiresphere-network
    ---
    apiVersion: v1
    kind: Namespace
    metadata:
      name: hiresphere-interview
    ---
    apiVersion: v1
    kind: Namespace
    metadata:
      name: hiresphere-profile
    ---
    apiVersion: v1
    kind: Namespace
    metadata:
      name: hiresphere-hr-studio
    ---
    apiVersion: v1
    kind: Namespace
    metadata:
      name: hiresphere-scale
    ---
    apiVersion: argoproj.io/v1alpha1
    kind: AppProject
    metadata:
      name: hiresphere-project
      namespace: argocd
    spec:
      description: HireSphere per-service GitOps project
      sourceRepos:
        - {repo_url}
      destinations:
        - namespace: argocd
          server: https://kubernetes.default.svc
        - namespace: hiresphere
          server: https://kubernetes.default.svc
        - namespace: hiresphere-gateway
          server: https://kubernetes.default.svc
        - namespace: hiresphere-api
          server: https://kubernetes.default.svc
        - namespace: hiresphere-workspace
          server: https://kubernetes.default.svc
        - namespace: hiresphere-jobs
          server: https://kubernetes.default.svc
        - namespace: hiresphere-projects
          server: https://kubernetes.default.svc
        - namespace: hiresphere-network
          server: https://kubernetes.default.svc
        - namespace: hiresphere-interview
          server: https://kubernetes.default.svc
        - namespace: hiresphere-profile
          server: https://kubernetes.default.svc
        - namespace: hiresphere-hr-studio
          server: https://kubernetes.default.svc
        - namespace: hiresphere-scale
          server: https://kubernetes.default.svc
      clusterResourceWhitelist:
        - group: ''
          kind: Namespace
        - group: ''
          kind: Service
        - group: apps
          kind: Deployment
        - group: networking.k8s.io
          kind: Ingress
      namespaceResourceWhitelist:
        - group: ''
          kind: ConfigMap
        - group: ''
          kind: Secret
        - group: ''
          kind: Service
        - group: ''
          kind: ServiceAccount
        - group: apps
          kind: Deployment
        - group: apps
          kind: StatefulSet
        - group: autoscaling
          kind: HorizontalPodAutoscaler
        - group: networking.k8s.io
          kind: Ingress
    """,
)

applications_dir = root / "argocd-applications"
for service_name, _, chart_name in services:
    app_name = service_name
    namespace = namespace_map[service_name]
    write(
        applications_dir / f"{service_name}.yaml",
        f"""
        apiVersion: argoproj.io/v1alpha1
        kind: Application
        metadata:
          name: {app_name}
          namespace: argocd
        spec:
          project: hiresphere-project
          source:
            repoURL: {repo_url}
            targetRevision: main
            path: charts/{chart_name}
          destination:
            server: https://kubernetes.default.svc
            namespace: {namespace}
          syncPolicy:
            automated:
              prune: true
              selfHeal: true
            syncOptions:
              - CreateNamespace=true
              - ApplyOutOfSyncOnly=true
        """,
    )

write(
    applications_dir / "hiresphere.yaml",
    f"""
    apiVersion: argoproj.io/v1alpha1
    kind: Application
    metadata:
      name: hiresphere
      namespace: argocd
    spec:
      project: hiresphere-project
      source:
        repoURL: {repo_url}
        targetRevision: main
        path: charts/hiresphere
        helm:
          valueFiles:
            - values-prod.yaml
      destination:
        server: https://kubernetes.default.svc
        namespace: hiresphere
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
        syncOptions:
          - CreateNamespace=true
          - ApplyOutOfSyncOnly=true
    """,
)

print("Generated per-service GitOps files.")
