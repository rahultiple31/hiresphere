FROM nginx:1.27-alpine

LABEL org.opencontainers.image.title="HireSphere"
LABEL org.opencontainers.image.description="Static hiring, freelancing, interview, and professional network platform UI"

# Copy nginx server config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy static files
COPY index.html /usr/share/nginx/html/
COPY styles.css /usr/share/nginx/html/
COPY app.js /usr/share/nginx/html/
COPY assets /usr/share/nginx/html/assets/

# Create nginx runtime directories and permissions
RUN mkdir -p \
    /var/cache/nginx/client_temp \
    /var/cache/nginx/proxy_temp \
    /var/cache/nginx/fastcgi_temp \
    /var/cache/nginx/uwsgi_temp \
    /var/cache/nginx/scgi_temp \
    /var/run/nginx \
    /tmp/nginx \
 && chown -R nginx:nginx \
    /usr/share/nginx/html \
    /var/cache/nginx \
    /var/run \
    /tmp/nginx \
    /etc/nginx \
 && chmod -R 755 /usr/share/nginx/html

# Run as non-root user
USER nginx

EXPOSE 8080

CMD ["nginx","-g","daemon off;"]
