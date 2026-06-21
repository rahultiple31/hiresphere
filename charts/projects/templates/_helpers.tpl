{{- define "projects.fullname" -}}
{{- .Release.Name }}-projects
{{- end }}

{{- define "projects.labels" -}}
app.kubernetes.io/name: projects
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/component: projects
{{- end }}
