{{- define "interview.fullname" -}}
{{- .Release.Name }}-interview
{{- end }}

{{- define "interview.labels" -}}
app.kubernetes.io/name: interview
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/component: interview
{{- end }}
