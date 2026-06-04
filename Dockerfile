FROM nginx:1.27-alpine

LABEL org.opencontainers.image.title="HireSphere"
LABEL org.opencontainers.image.description="Static hiring, freelancing, interview, and professional network platform UI"

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY index.html /usr/share/nginx/html/index.html
COPY styles.css /usr/share/nginx/html/styles.css
COPY app.js /usr/share/nginx/html/app.js
COPY assets /usr/share/nginx/html/assets

RUN mkdir -p /var/cache/nginx/client_temp \
    /var/cache/nginx/proxy_temp \
    /var/cache/nginx/fastcgi_temp \
    /var/cache/nginx/uwsgi_temp \
    /var/cache/nginx/scgi_temp \
    /var/run \
  && chown -R nginx:nginx /usr/share/nginx/html \
    /var/cache/nginx \
    /var/run \
    /var/log/nginx \
    /etc/nginx/conf.d \
  && chmod -R 755 /usr/share/nginx/html

USER nginx

EXPOSE 8080

CMD ["nginx", "-g", "pid /tmp/nginx.pid; daemon off;"]
