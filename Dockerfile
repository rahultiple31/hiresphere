FROM nginx:1.27-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY index.html /usr/share/nginx/html/
COPY styles.css /usr/share/nginx/html/
COPY app.js /usr/share/nginx/html/
COPY assets /usr/share/nginx/html/assets/

RUN mkdir -p /var/cache/nginx \
    /var/run \
    /tmp/nginx \
 && chown -R nginx:nginx \
    /usr/share/nginx/html \
    /var/cache/nginx \
    /var/run \
    /tmp/nginx \
    /etc/nginx

EXPOSE 8080

USER nginx

CMD ["nginx", "-g", "daemon off; pid /tmp/nginx/nginx.pid;"]
