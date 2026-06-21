{{- define "workspace.fullname" -}}
workspace-service
{{- end }}

{{- define "workspace.labels" -}}
app.kubernetes.io/name: workspace
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/component: workspace
{{- end }}
