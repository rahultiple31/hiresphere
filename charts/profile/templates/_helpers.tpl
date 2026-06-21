{{- define "profile.fullname" -}}
{{- .Release.Name }}-profile
{{- end }}

{{- define "profile.labels" -}}
app.kubernetes.io/name: profile
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/component: profile
{{- end }}
