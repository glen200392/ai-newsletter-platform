# AWS Deployment Guide
## AI Newsletter Platform on AWS

This guide provides step-by-step instructions for deploying the AI Newsletter Platform on AWS using ECS Fargate, RDS, and other managed services.

---

## Architecture Overview

```
Internet
    │
    ▼
CloudFront (CDN + SSL)
    │
    ▼
Application Load Balancer
    │
    ├─► ECS Fargate (API Tasks)
    │   └─► Task 1, Task 2, Task 3...
    │
    ├─► ECS Fargate (Worker Tasks)
    │   └─► Celery Workers
    │
    ├─► RDS PostgreSQL (Multi-AZ)
    │
    ├─► ElastiCache Redis
    │
    └─► S3 (Static Assets & Backups)
```

---

## Prerequisites

- AWS Account with appropriate permissions
- AWS CLI installed and configured
- Docker installed locally
- Domain name (for SSL/TLS)

---

## Step 1: Setup AWS CLI

```bash
# Install AWS CLI (if not already installed)
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Configure AWS CLI
aws configure
# AWS Access Key ID: YOUR_ACCESS_KEY
# AWS Secret Access Key: YOUR_SECRET_KEY
# Default region name: us-east-1
# Default output format: json
```

---

## Step 2: Create ECR Repository

```bash
# Create ECR repository for Docker images
aws ecr create-repository \
    --repository-name newsletter-platform \
    --region us-east-1

# Get repository URI
ECR_URI=$(aws ecr describe-repositories \
    --repository-names newsletter-platform \
    --query 'repositories[0].repositoryUri' \
    --output text)

echo "ECR URI: $ECR_URI"
```

---

## Step 3: Build and Push Docker Image

```bash
# Authenticate Docker to ECR
aws ecr get-login-password --region us-east-1 | \
    docker login --username AWS --password-stdin $ECR_URI

# Build Docker image
docker build -t newsletter-platform:latest .

# Tag image
docker tag newsletter-platform:latest $ECR_URI:latest
docker tag newsletter-platform:latest $ECR_URI:v1.0.0

# Push to ECR
docker push $ECR_URI:latest
docker push $ECR_URI:v1.0.0
```

---

## Step 4: Create VPC and Networking

```bash
# Create VPC
VPC_ID=$(aws ec2 create-vpc \
    --cidr-block 10.0.0.0/16 \
    --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=newsletter-vpc}]' \
    --query 'Vpc.VpcId' \
    --output text)

# Create Internet Gateway
IGW_ID=$(aws ec2 create-internet-gateway \
    --tag-specifications 'ResourceType=internet-gateway,Tags=[{Key=Name,Value=newsletter-igw}]' \
    --query 'InternetGateway.InternetGatewayId' \
    --output text)

# Attach IGW to VPC
aws ec2 attach-internet-gateway \
    --vpc-id $VPC_ID \
    --internet-gateway-id $IGW_ID

# Create Public Subnets (2 AZs for high availability)
SUBNET_PUBLIC_1=$(aws ec2 create-subnet \
    --vpc-id $VPC_ID \
    --cidr-block 10.0.1.0/24 \
    --availability-zone us-east-1a \
    --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=newsletter-public-1a}]' \
    --query 'Subnet.SubnetId' \
    --output text)

SUBNET_PUBLIC_2=$(aws ec2 create-subnet \
    --vpc-id $VPC_ID \
    --cidr-block 10.0.2.0/24 \
    --availability-zone us-east-1b \
    --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=newsletter-public-1b}]' \
    --query 'Subnet.SubnetId' \
    --output text)

# Create Private Subnets
SUBNET_PRIVATE_1=$(aws ec2 create-subnet \
    --vpc-id $VPC_ID \
    --cidr-block 10.0.11.0/24 \
    --availability-zone us-east-1a \
    --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=newsletter-private-1a}]' \
    --query 'Subnet.SubnetId' \
    --output text)

SUBNET_PRIVATE_2=$(aws ec2 create-subnet \
    --vpc-id $VPC_ID \
    --cidr-block 10.0.12.0/24 \
    --availability-zone us-east-1b \
    --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=newsletter-private-1b}]' \
    --query 'Subnet.SubnetId' \
    --output text)

# Create Route Table for Public Subnets
RT_PUBLIC=$(aws ec2 create-route-table \
    --vpc-id $VPC_ID \
    --tag-specifications 'ResourceType=route-table,Tags=[{Key=Name,Value=newsletter-public-rt}]' \
    --query 'RouteTable.RouteTableId' \
    --output text)

# Add route to Internet Gateway
aws ec2 create-route \
    --route-table-id $RT_PUBLIC \
    --destination-cidr-block 0.0.0.0/0 \
    --gateway-id $IGW_ID

# Associate public subnets with route table
aws ec2 associate-route-table --subnet-id $SUBNET_PUBLIC_1 --route-table-id $RT_PUBLIC
aws ec2 associate-route-table --subnet-id $SUBNET_PUBLIC_2 --route-table-id $RT_PUBLIC
```

---

## Step 5: Create RDS PostgreSQL Database

```bash
# Create DB Subnet Group
aws rds create-db-subnet-group \
    --db-subnet-group-name newsletter-db-subnet \
    --db-subnet-group-description "Newsletter Platform DB Subnet Group" \
    --subnet-ids $SUBNET_PRIVATE_1 $SUBNET_PRIVATE_2

# Create Security Group for RDS
RDS_SG=$(aws ec2 create-security-group \
    --group-name newsletter-rds-sg \
    --description "Security group for Newsletter RDS" \
    --vpc-id $VPC_ID \
    --query 'GroupId' \
    --output text)

# Allow PostgreSQL traffic from ECS
aws ec2 authorize-security-group-ingress \
    --group-id $RDS_SG \
    --protocol tcp \
    --port 5432 \
    --source-group $ECS_SG

# Create RDS Instance
aws rds create-db-instance \
    --db-instance-identifier newsletter-db \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --engine-version 15.4 \
    --master-username newsletter_admin \
    --master-user-password 'ChangeThisPassword!' \
    --allocated-storage 20 \
    --storage-type gp3 \
    --vpc-security-group-ids $RDS_SG \
    --db-subnet-group-name newsletter-db-subnet \
    --backup-retention-period 7 \
    --multi-az \
    --publicly-accessible false \
    --storage-encrypted

# Get RDS endpoint (wait for creation to complete)
aws rds wait db-instance-available --db-instance-identifier newsletter-db

RDS_ENDPOINT=$(aws rds describe-db-instances \
    --db-instance-identifier newsletter-db \
    --query 'DBInstances[0].Endpoint.Address' \
    --output text)

echo "RDS Endpoint: $RDS_ENDPOINT"
```

---

## Step 6: Create ElastiCache Redis

```bash
# Create Redis Subnet Group
aws elasticache create-cache-subnet-group \
    --cache-subnet-group-name newsletter-redis-subnet \
    --cache-subnet-group-description "Newsletter Platform Redis Subnet Group" \
    --subnet-ids $SUBNET_PRIVATE_1 $SUBNET_PRIVATE_2

# Create Security Group for Redis
REDIS_SG=$(aws ec2 create-security-group \
    --group-name newsletter-redis-sg \
    --description "Security group for Newsletter Redis" \
    --vpc-id $VPC_ID \
    --query 'GroupId' \
    --output text)

# Allow Redis traffic from ECS
aws ec2 authorize-security-group-ingress \
    --group-id $REDIS_SG \
    --protocol tcp \
    --port 6379 \
    --source-group $ECS_SG

# Create Redis Cluster
aws elasticache create-cache-cluster \
    --cache-cluster-id newsletter-redis \
    --engine redis \
    --engine-version 7.0 \
    --cache-node-type cache.t3.micro \
    --num-cache-nodes 1 \
    --cache-subnet-group-name newsletter-redis-subnet \
    --security-group-ids $REDIS_SG

# Get Redis endpoint
aws elasticache wait cache-cluster-available --cache-cluster-id newsletter-redis

REDIS_ENDPOINT=$(aws elasticache describe-cache-clusters \
    --cache-cluster-id newsletter-redis \
    --show-cache-node-info \
    --query 'CacheClusters[0].CacheNodes[0].Endpoint.Address' \
    --output text)

echo "Redis Endpoint: $REDIS_ENDPOINT"
```

---

## Step 7: Create ECS Cluster

```bash
# Create ECS Cluster
aws ecs create-cluster \
    --cluster-name newsletter-cluster \
    --capacity-providers FARGATE FARGATE_SPOT \
    --default-capacity-provider-strategy \
        capacityProvider=FARGATE,weight=1,base=1 \
        capacityProvider=FARGATE_SPOT,weight=4

# Create Security Group for ECS Tasks
ECS_SG=$(aws ec2 create-security-group \
    --group-name newsletter-ecs-sg \
    --description "Security group for Newsletter ECS tasks" \
    --vpc-id $VPC_ID \
    --query 'GroupId' \
    --output text)

# Allow HTTP traffic from ALB
aws ec2 authorize-security-group-ingress \
    --group-id $ECS_SG \
    --protocol tcp \
    --port 8000 \
    --source-group $ALB_SG
```

---

## Step 8: Create Application Load Balancer

```bash
# Create Security Group for ALB
ALB_SG=$(aws ec2 create-security-group \
    --group-name newsletter-alb-sg \
    --description "Security group for Newsletter ALB" \
    --vpc-id $VPC_ID \
    --query 'GroupId' \
    --output text)

# Allow HTTP and HTTPS from anywhere
aws ec2 authorize-security-group-ingress \
    --group-id $ALB_SG \
    --protocol tcp \
    --port 80 \
    --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress \
    --group-id $ALB_SG \
    --protocol tcp \
    --port 443 \
    --cidr 0.0.0.0/0

# Create ALB
ALB_ARN=$(aws elbv2 create-load-balancer \
    --name newsletter-alb \
    --subnets $SUBNET_PUBLIC_1 $SUBNET_PUBLIC_2 \
    --security-groups $ALB_SG \
    --scheme internet-facing \
    --type application \
    --ip-address-type ipv4 \
    --query 'LoadBalancers[0].LoadBalancerArn' \
    --output text)

# Create Target Group
TG_ARN=$(aws elbv2 create-target-group \
    --name newsletter-tg \
    --protocol HTTP \
    --port 8000 \
    --vpc-id $VPC_ID \
    --target-type ip \
    --health-check-path /health \
    --health-check-interval-seconds 30 \
    --health-check-timeout-seconds 5 \
    --healthy-threshold-count 2 \
    --unhealthy-threshold-count 3 \
    --query 'TargetGroups[0].TargetGroupArn' \
    --output text)

# Create Listener
aws elbv2 create-listener \
    --load-balancer-arn $ALB_ARN \
    --protocol HTTP \
    --port 80 \
    --default-actions Type=forward,TargetGroupArn=$TG_ARN
```

---

## Step 9: Create ECS Task Definition

Create `task-definition.json`:

```json
{
  "family": "newsletter-api",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::YOUR_ACCOUNT_ID:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::YOUR_ACCOUNT_ID:role/ecsTaskRole",
  "containerDefinitions": [
    {
      "name": "newsletter-api",
      "image": "YOUR_ECR_URI:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "APP_ENV",
          "value": "production"
        },
        {
          "name": "DATABASE_URL",
          "value": "postgresql://newsletter_admin:PASSWORD@RDS_ENDPOINT:5432/newsletter_db"
        },
        {
          "name": "REDIS_URL",
          "value": "redis://REDIS_ENDPOINT:6379/0"
        }
      ],
      "secrets": [
        {
          "name": "OPENAI_API_KEY",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:ACCOUNT_ID:secret:newsletter/openai-key"
        },
        {
          "name": "SENDGRID_API_KEY",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:ACCOUNT_ID:secret:newsletter/sendgrid-key"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/newsletter-api",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "api"
        }
      },
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:8000/health || exit 1"],
        "interval": 30,
        "timeout": 5,
        "retries": 3,
        "startPeriod": 60
      }
    }
  ]
}
```

Register task definition:

```bash
aws ecs register-task-definition --cli-input-json file://task-definition.json
```

---

## Step 10: Create ECS Service

```bash
aws ecs create-service \
    --cluster newsletter-cluster \
    --service-name newsletter-api-service \
    --task-definition newsletter-api \
    --desired-count 2 \
    --launch-type FARGATE \
    --platform-version LATEST \
    --network-configuration "awsvpcConfiguration={subnets=[$SUBNET_PRIVATE_1,$SUBNET_PRIVATE_2],securityGroups=[$ECS_SG],assignPublicIp=DISABLED}" \
    --load-balancers "targetGroupArn=$TG_ARN,containerName=newsletter-api,containerPort=8000" \
    --health-check-grace-period-seconds 60 \
    --enable-execute-command
```

---

## Step 11: Setup Auto Scaling

```bash
# Register scalable target
aws application-autoscaling register-scalable-target \
    --service-namespace ecs \
    --scalable-dimension ecs:service:DesiredCount \
    --resource-id service/newsletter-cluster/newsletter-api-service \
    --min-capacity 2 \
    --max-capacity 10

# Create scaling policy
aws application-autoscaling put-scaling-policy \
    --service-namespace ecs \
    --scalable-dimension ecs:service:DesiredCount \
    --resource-id service/newsletter-cluster/newsletter-api-service \
    --policy-name newsletter-cpu-scaling \
    --policy-type TargetTrackingScaling \
    --target-tracking-scaling-policy-configuration file://scaling-policy.json
```

`scaling-policy.json`:
```json
{
  "TargetValue": 75.0,
  "PredefinedMetricSpecification": {
    "PredefinedMetricType": "ECSServiceAverageCPUUtilization"
  },
  "ScaleInCooldown": 300,
  "ScaleOutCooldown": 60
}
```

---

## Step 12: Setup CloudWatch Alarms

```bash
# High CPU alarm
aws cloudwatch put-metric-alarm \
    --alarm-name newsletter-high-cpu \
    --alarm-description "Alert when CPU exceeds 80%" \
    --metric-name CPUUtilization \
    --namespace AWS/ECS \
    --statistic Average \
    --period 300 \
    --threshold 80 \
    --comparison-operator GreaterThanThreshold \
    --evaluation-periods 2

# Database connections alarm
aws cloudwatch put-metric-alarm \
    --alarm-name newsletter-db-connections \
    --alarm-description "Alert when DB connections exceed 80" \
    --metric-name DatabaseConnections \
    --namespace AWS/RDS \
    --statistic Average \
    --period 300 \
    --threshold 80 \
    --comparison-operator GreaterThanThreshold \
    --evaluation-periods 1
```

---

## Step 13: Verify Deployment

```bash
# Get ALB DNS name
ALB_DNS=$(aws elbv2 describe-load-balancers \
    --load-balancer-arns $ALB_ARN \
    --query 'LoadBalancers[0].DNSName' \
    --output text)

echo "Application URL: http://$ALB_DNS"

# Test health endpoint
curl http://$ALB_DNS/health

# Expected response:
# {"status":"healthy","timestamp":"...","version":"1.0.0"}
```

---

## Cost Estimation

**Monthly costs (us-east-1, approximate)**:

| Service | Configuration | Monthly Cost |
|---------|---------------|--------------|
| ECS Fargate | 2 tasks (0.5 vCPU, 1GB RAM) | $35 |
| RDS PostgreSQL | db.t3.micro, Multi-AZ, 20GB | $30 |
| ElastiCache Redis | cache.t3.micro | $15 |
| Application Load Balancer | Standard | $23 |
| Data Transfer | 100GB out | $9 |
| CloudWatch Logs | 10GB ingestion | $5 |
| **Total** | | **~$117/month** |

*Note: Costs vary based on usage. Use AWS Cost Calculator for accurate estimates.*

---

## Maintenance

### Update Application

```bash
# Build and push new image
docker build -t newsletter-platform:v1.1.0 .
docker tag newsletter-platform:v1.1.0 $ECR_URI:v1.1.0
docker push $ECR_URI:v1.1.0

# Update service with new image
aws ecs update-service \
    --cluster newsletter-cluster \
    --service newsletter-api-service \
    --force-new-deployment
```

### Backup Database

```bash
# Create manual snapshot
aws rds create-db-snapshot \
    --db-instance-identifier newsletter-db \
    --db-snapshot-identifier newsletter-db-snapshot-$(date +%Y%m%d)
```

### View Logs

```bash
# Stream logs
aws logs tail /ecs/newsletter-api --follow
```

---

## Cleanup

To remove all resources:

```bash
# Delete ECS service
aws ecs delete-service --cluster newsletter-cluster --service newsletter-api-service --force

# Delete ECS cluster
aws ecs delete-cluster --cluster newsletter-cluster

# Delete RDS instance
aws rds delete-db-instance --db-instance-identifier newsletter-db --skip-final-snapshot

# Delete ElastiCache cluster
aws elasticache delete-cache-cluster --cache-cluster-id newsletter-redis

# Delete load balancer and target group
aws elbv2 delete-load-balancer --load-balancer-arn $ALB_ARN
aws elbv2 delete-target-group --target-group-arn $TG_ARN

# Delete VPC and networking (after all resources deleted)
# ... (omitted for brevity)
```

---

## Troubleshooting

### Tasks fail to start
- Check CloudWatch Logs: `/ecs/newsletter-api`
- Verify environment variables and secrets
- Ensure security groups allow traffic

### Database connection issues
- Verify RDS endpoint and credentials
- Check security group rules
- Test from ECS task: `aws ecs execute-command`

### High latency
- Enable CloudFront for CDN caching
- Check RDS performance insights
- Review ECS task CPU/memory metrics

---

## Next Steps

- [ ] Setup CloudFront CDN
- [ ] Configure Route53 for custom domain
- [ ] Enable AWS WAF for security
- [ ] Setup automated backups to S3
- [ ] Configure CI/CD with CodePipeline
