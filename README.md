# Flower Bouquet Shop - AWS 3-Tier DevOps Project

A simple flower bouquet e-commerce application using:
- Frontend: HTML/CSS/JavaScript in one index.html
- Backend: Python Flask REST API
- Database: MySQL (local Docker for development, Amazon RDS for AWS)
- Containerization: Docker + one docker-compose.yml
- Image management: Amazon ECR
- CI/CD: Jenkins
- Source control: Git/GitHub

## Project structure

flower-bouquet-shop/
├── frontend/
│   ├── index.html
│   └── Dockerfile
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── database/
│   └── init.sql
├── nginx/
│   └── nginx.conf
├── docker-compose.yml
├── Jenkinsfile
├── .env.example
├── .gitignore
└── README.md

## Local Docker test

1. Copy `.env.example` to `.env`.
2. Run:
   docker compose up --build -d
3. Check:
   docker compose ps
4. Open:
   http://localhost
5. API health:
   http://localhost/api/health

## AWS deployment concept

For AWS, the same `docker-compose.yml` can run images from ECR by setting:
ECR_REGISTRY, IMAGE_TAG, DB_HOST, DB_NAME, DB_USER, DB_PASSWORD.

Use Amazon RDS for the database in AWS. Do not expose RDS publicly.

## Security

Never commit `.env`, AWS access keys, private keys, or real database passwords.
