{{- define "hr-studio.fullname" -}}
{{- .Release.Name }}-hr-studio
{{- end }}

{{- define "hr-studio.labels" -}}
app.kubernetes.io/name: hr-studio
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/component: hr-studio
{{- end }}
