{{- define "hr-studio.fullname" -}}
hr-studio-service
{{- end }}

{{- define "hr-studio.labels" -}}
app.kubernetes.io/name: hr-studio
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/component: hr-studio
{{- end }}
