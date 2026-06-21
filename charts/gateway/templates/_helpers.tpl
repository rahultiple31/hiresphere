{{- define "gateway.fullname" -}}
{{- .Release.Name }}-gateway
{{- end }}

{{- define "gateway.labels" -}}
app.kubernetes.io/name: gateway
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/component: gateway
{{- end }}
