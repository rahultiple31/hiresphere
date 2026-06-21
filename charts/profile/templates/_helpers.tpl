{{- define "profile.fullname" -}}
profile-service
{{- end }}

{{- define "profile.labels" -}}
app.kubernetes.io/name: profile
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/component: profile
{{- end }}
