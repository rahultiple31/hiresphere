{{- define "projects.fullname" -}}
projects-service
{{- end }}

{{- define "projects.labels" -}}
app.kubernetes.io/name: projects
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/component: projects
{{- end }}
