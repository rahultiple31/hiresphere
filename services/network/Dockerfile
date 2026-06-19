FROM nginxinc/nginx-unprivileged:1.27-alpine

LABEL org.opencontainers.image.title="HireSphere Network Service"
LABEL org.opencontainers.image.description="Network micro-frontend for HireSphere"

USER root
COPY --chown=101:101 services/nginx.conf /etc/nginx/conf.d/default.conf
COPY --chown=101:101 services/network/index.html /usr/share/nginx/html/index.html
COPY --chown=101:101 services/network/app.js /usr/share/nginx/html/app.js
COPY --chown=101:101 services/network/styles.css /usr/share/nginx/html/styles.css
RUN chmod -R 755 /usr/share/nginx/html
USER 101:101
EXPOSE 8080
HEALTHCHECK --interval=20s --timeout=3s --start-period=5s --retries=3 CMD wget -qO- http://127.0.0.1:8080/healthz || exit 1
CMD ["nginx", "-g", "daemon off;"]
