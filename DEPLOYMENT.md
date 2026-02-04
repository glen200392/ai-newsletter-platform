# Deployment Guide

## Quick Start (Local Development)

```bash
# Clone repository
git clone https://github.com/yourusername/ai-newsletter-platform.git
cd ai-newsletter-platform

# Set environment variables
cp env.example .env
# Edit .env with your configuration

# Start services
docker-compose up -d

# Check status
docker-compose ps
```

## Production Deployment

### GCP Deployment

```bash
# 1. Set up GCP credentials
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# 2. Deploy infrastructure
cd infrastructure/terraform/gcp
terraform init
terraform apply

# 3. Deploy application
cd ../../..
kubectl apply -f infrastructure/kubernetes/base/
```

### Azure Deployment

```bash
# 1. Login to Azure
az login

# 2. Deploy infrastructure
cd infrastructure/terraform/azure
terraform init
terraform apply

# 3. Deploy application
kubectl apply -f infrastructure/kubernetes/base/
```

## Monitoring

Access dashboards:
- Grafana: http://localhost:3000 (admin/admin)
- Prometheus: http://localhost:9090

## Troubleshooting

### Common Issues

1. **Database connection failed**
   - Check DATABASE_URL in .env
   - Ensure PostgreSQL is running

2. **Message queue errors**
   - Verify RabbitMQ is accessible
   - Check MESSAGE_QUEUE_URL

For more help, see documentation or open an issue.
