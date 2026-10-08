# ==============================================================================
# DWPG Simulator Backend - Hardened Alpine JRE 21 Container
# Course: 24CYS401 Secure Software Engineering
# ==============================================================================

FROM eclipse-temurin:21-jre-alpine AS runtime

LABEL maintainer="sathvikvalivety" \
      project="dwpg-simulator" \
      security.hardened="true"

# Create unprivileged system group and user (UID/GID 10001)
RUN addgroup -g 10001 -S appgroup && \
    adduser -u 10001 -S appuser -G appgroup

WORKDIR /app

# Copy runnable fat JAR with proper ownership
COPY --chown=appuser:appgroup target/dwpg-simulator-1.0.0.jar /app/dwpg-simulator.jar

# Enforce least privilege execution
USER 10001:10001

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/actuator/health || exit 1

ENTRYPOINT ["java", \
  "-XX:+UseContainerSupport", \
  "-XX:MaxRAMPercentage=75.0", \
  "-Djava.security.egd=file:/dev/./urandom", \
  "-jar", "/app/dwpg-simulator.jar"]
