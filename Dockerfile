FROM nginxinc/nginx-unprivileged:1.27-alpine

LABEL org.opencontainers.image.title="HireSphere Gateway"
LABEL org.opencontainers.image.description="Shell and reverse proxy for HireSphere micro-frontends"

USER root
COPY --chown=101:101 gateway/nginx.conf /etc/nginx/conf.d/default.conf
COPY --chown=101:101 gateway/index.html /usr/share/nginx/html/index.html
COPY --chown=101:101 gateway/app.js /usr/share/nginx/html/shell.js
COPY --chown=101:101 gateway/styles.css /usr/share/nginx/html/shell.css
COPY --chown=101:101 services/shared /usr/share/nginx/html/shared
COPY --chown=101:101 assets /usr/share/nginx/html/assets
RUN chmod -R 755 /usr/share/nginx/html
USER 101:101
EXPOSE 8080
HEALTHCHECK --interval=20s --timeout=3s --start-period=5s --retries=3 CMD wget -qO- http://127.0.0.1:8080/healthz || exit 1
CMD ["nginx", "-g", "daemon off;"]
