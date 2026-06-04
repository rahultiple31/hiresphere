FROM nginxinc/nginx-unprivileged:1.27-alpine

LABEL org.opencontainers.image.title="HireSphere"
LABEL org.opencontainers.image.description="Static hiring, freelancing, interview, and professional network platform UI"

USER root

COPY --chown=101:101 nginx.conf /etc/nginx/conf.d/default.conf
COPY --chown=101:101 index.html /usr/share/nginx/html/index.html
COPY --chown=101:101 styles.css /usr/share/nginx/html/styles.css
COPY --chown=101:101 app.js /usr/share/nginx/html/app.js
COPY --chown=101:101 assets /usr/share/nginx/html/assets

RUN chmod -R 755 /usr/share/nginx/html

USER 101:101

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
