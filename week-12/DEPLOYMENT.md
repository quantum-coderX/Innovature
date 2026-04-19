# Week 12 Deployment Guide (Render)

This guide uses Render as the deployment target with managed PostgreSQL and optional S3 media storage.

## 1. Prerequisites

- Python 3.11+
- A PostgreSQL database (managed cloud DB recommended)
- A Render account
- Optional: S3 bucket for media files

## 2. Environment Setup

Set these variables in your cloud dashboard (not in source control):

- `APP_ENV=production`
- `FLASK_ENV=production`
- `DATABASE_URL=<managed-postgres-url>`
- `JWT_SECRET_KEY=<long-random-secret>`
- `API_PORT=5000` (optional, cloud often injects `PORT`)

For local-disk media (default):

- `STORAGE_BACKEND=local`

For S3 media (bonus):

- `STORAGE_BACKEND=s3`
- `AWS_S3_BUCKET=<your-bucket-name>`
- `AWS_REGION=<bucket-region>`
- `AWS_ACCESS_KEY_ID=<aws-key-id>`
- `AWS_SECRET_ACCESS_KEY=<aws-secret-key>`
- Optional `S3_CUSTOM_DOMAIN=<cdn-or-custom-domain>`
- Optional `S3_MEDIA_PREFIX=uploads`

## 3. Render Deployment (Recommended Path)

1. Push `week-12` to your Git provider.
2. In Render, create a new Blueprint service from your repository.
3. Render automatically reads `render.yaml` from the repo root.
4. Confirm service settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn main:app --bind 0.0.0.0:$PORT`
  - Root Directory: `week-12`
5. Let Render create the `week12-ecommerce-db` managed PostgreSQL database from `render.yaml`.
6. Add/confirm environment variables in Render:
  - `APP_ENV=production`
  - `FLASK_ENV=production`
  - `JWT_SECRET_KEY=<strong-random-value>`
  - `STORAGE_BACKEND=local` (or `s3` for bonus)
  - `DATABASE_URL` is auto-injected from the Render database mapping
7. Deploy and wait for build + health check success.
8. Verify `GET /` on the generated Render URL.

## 4. Optional S3 Configuration (Bonus)

If you want cloud object storage instead of local disk storage:

1. Set `STORAGE_BACKEND=s3` in Render env vars.
2. Add these env vars:
  - `AWS_S3_BUCKET`
  - `AWS_REGION`
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`
3. Optional:
  - `S3_MEDIA_PREFIX` (default `uploads`)
  - `S3_CUSTOM_DOMAIN` (if using CDN/custom media domain)
4. Redeploy and test image upload endpoint.

## 5. Production Database Notes (Render Postgres)

- Render Postgres is already provisioned via `render.yaml`.
- Keep DB credentials managed by Render; do not hardcode secrets in files.
- Enable backups in Render database settings if your plan supports it.

## 6. Validation Checklist

- App deploy succeeds on Render.
- `GET /` returns status `ok`.
- Register/login endpoints work.
- Product/category/cart endpoints work with Render Postgres.
- Image upload works:
  - local mode if `STORAGE_BACKEND=local`
  - S3 URLs if `STORAGE_BACKEND=s3`

## 7. Deliverables (for Submission)

- Live app URL: `https://<your-render-service>.onrender.com`
- Repository: `<your-repo-url>`
- Deployment guide: this file (`week-12/DEPLOYMENT.md`)

