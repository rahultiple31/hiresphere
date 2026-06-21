{{- define "jobs.fullname" -}}
{{- .Release.Name }}-jobs
{{- end }}

{{- define "jobs.labels" -}}
app.kubernetes.io/name: jobs
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/component: jobs
{{- end }}
