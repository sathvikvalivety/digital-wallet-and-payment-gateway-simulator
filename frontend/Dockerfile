# ==============================================================================
# DWPG Simulator Frontend - Hardened Unprivileged Nginx Container
# Course: 24CYS401 Secure Software Engineering
# ==============================================================================

FROM nginxinc/nginx-unprivileged:alpine AS runtime

LABEL maintainer="sathvikvalivety" \
      project="dwpg-simulator-frontend" \
      security.hardened="true"

# Copy compiled static distribution bundle
COPY dist /usr/share/nginx/html

# Copy custom hardened virtual host configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://127.0.0.1:3000/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
