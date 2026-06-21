{{- define "workspace.fullname" -}}
{{- .Release.Name }}-workspace
{{- end }}

{{- define "workspace.labels" -}}
app.kubernetes.io/name: workspace
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/component: workspace
{{- end }}
