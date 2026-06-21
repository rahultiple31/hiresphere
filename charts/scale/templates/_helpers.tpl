{{- define "scale.fullname" -}}
scale-service
{{- end }}

{{- define "scale.labels" -}}
app.kubernetes.io/name: scale
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/component: scale
{{- end }}
