{{- define "network.fullname" -}}
{{- .Release.Name }}-network
{{- end }}

{{- define "network.labels" -}}
app.kubernetes.io/name: network
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/component: network
{{- end }}
