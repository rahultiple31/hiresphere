{{- define "api.fullname" -}}
{{- .Release.Name }}-api
{{- end }}

{{- define "api.labels" -}}
app.kubernetes.io/name: api
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/component: api
{{- end }}
