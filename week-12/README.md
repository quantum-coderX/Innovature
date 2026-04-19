# Week 12 - Deployment (Cloud-Ready E-commerce Backend)

This week delivers a production-ready deployment package for the existing Flask e-commerce API.

## Assignment Coverage

- Deploy backend to a cloud service: Render (chosen platform).
- Configure environment variables for development and production.
- Use a production PostgreSQL database.
- Bonus: support S3 storage for uploaded media.
- Deliverables included in this folder:
  - API source code
  - Deployment config files
  - Deployment guide

## What Is Included

- Environment-aware app configuration using `APP_ENV` / `FLASK_ENV`.
- Production-safe database URL handling (`postgres://` to `postgresql://` normalization).
- Gunicorn support for cloud web services.
- Render blueprint file (`render.yaml`) with web service + managed PostgreSQL.
- Optional S3 media backend for product images/thumbnails.

## Project Files Added for Deployment

- `render.yaml`
- `DEPLOYMENT.md`

## Environment Variables

Use `.env.example` as the source of truth.
For production-only reference values, use `.env.production.example`.

### Required for all environments

- `DATABASE_URL`
- `JWT_SECRET_KEY`
- `APP_ENV` (`development` or `production`)

### Required only for S3 mode

- `STORAGE_BACKEND=s3`
- `AWS_S3_BUCKET`
- `AWS_REGION`
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

Optional:

- `S3_CUSTOM_DOMAIN`
- `AWS_S3_ENDPOINT_URL`
- `S3_MEDIA_PREFIX`

## Local Run

1. Install dependencies:

```bash
cd week-12
pip install -r requirements.txt
```

2. Create environment file:

```bash
copy .env.example .env
```

3. Start PostgreSQL (optional local docker):

```bash
docker-compose up -d
```

4. Run API:

```bash
python main.py
```

Health endpoint: `GET /`

## Production Run Command

Cloud services should run:

```bash
gunicorn main:app --bind 0.0.0.0:$PORT
```

## Deployment Guide

Detailed Render steps are in `DEPLOYMENT.md`.

## Deliverable Checklist

- Live app URL: add after deployment
- Repo path: this `week-12` folder
- Deployment guide: `DEPLOYMENT.md`
