FROM nginx:1.27-alpine

LABEL org.opencontainers.image.title="HireSphere"
LABEL org.opencontainers.image.description="Static hiring, freelancing, interview, and professional network platform UI"

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy static files
COPY index.html /usr/share/nginx/html/
COPY styles.css /usr/share/nginx/html/
COPY app.js /usr/share/nginx/html/
COPY assets /usr/share/nginx/html/assets/

# Create required directories and permissions
RUN mkdir -p /var/cache/nginx \
    && mkdir -p /var/run \
    && mkdir -p /tmp/nginx \
    && chown -R nginx:nginx /usr/share/nginx/html \
    && chown -R nginx:nginx /var/cache/nginx \
    && chown -R nginx:nginx /var/run \
    && chown -R nginx:nginx /tmp/nginx \
    && chmod -R 755 /usr/share/nginx/html

# Run container as non-root
USER nginx

# Use 8080 because non-root cannot bind to port 80
EXPOSE 8080

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
