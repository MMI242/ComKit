# ============================================
# Stage 1: Base - Install dependencies
# ============================================
FROM node:22-bookworm-slim AS base

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm ci || npm install

# ============================================
# Stage 2: Test
# ============================================
FROM base AS test

COPY . .

RUN npx vitest run --reporter=verbose || true

# ============================================
# Stage 3: Build
# ============================================
FROM base AS build

COPY . .

ENV NITRO_PRESET=node-server
ENV API_BASE_URL=http://localhost:8000

RUN npm run build

# ============================================
# Stage 4: Production
# ============================================
FROM node:22-bookworm-slim AS production

WORKDIR /app

# Copy built output
COPY --from=build /app/.output /app/.output

# Non-root user for security
RUN adduser --disabled-password --gecos "" appuser && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 3000

ENV HOST=0.0.0.0
ENV PORT=3000

CMD ["node", ".output/server/index.mjs"]
