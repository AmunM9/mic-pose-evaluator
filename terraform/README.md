# Terraform — Infraestructura AWS para Mic&Pose Evaluator

> Este código define la infraestructura completa. **No se aplica automáticamente** — requiere credenciales AWS y revisión manual antes de `terraform apply`.

## Arquitectura

```
Internet
    │
    ▼
┌─────────────────────────────────────────────────────┐
│                   AWS us-east-1                      │
│                                                      │
│  ┌──────────┐    ┌───────────────────────────────┐  │
│  │CloudFront│    │           VPC 10.0.0.0/16      │  │
│  │(frontend)│    │                                │  │
│  └────┬─────┘    │  Subnets públicas (ALB)        │  │
│       │          │  ┌─────────────────────────┐   │  │
│       │          │  │  Application Load       │   │  │
│  ┌────▼─────┐    │  │  Balancer (HTTPS:443)   │   │  │
│  │ S3 bucket│    │  └────────────┬────────────┘   │  │
│  │(frontend)│    │               │                │  │
│  └──────────┘    │  Subnets privadas (ECS + RDS)  │  │
│                  │  ┌────────────▼────────────┐   │  │
│                  │  │  ECS Fargate            │   │  │
│                  │  │  FastAPI :8000          │   │  │
│                  │  │  (512 CPU / 1024 MB)    │   │  │
│                  │  └────────────┬────────────┘   │  │
│                  │               │                │  │
│                  │  ┌────────────▼────────────┐   │  │
│                  │  │  RDS PostgreSQL 16       │   │  │
│                  │  │  db.t4g.micro            │   │  │
│                  │  └─────────────────────────┘   │  │
│                  │                                │  │
│                  │  S3 bucket (audios)            │  │
│                  └───────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

## Decisiones de arquitectura

### ECS Fargate vs EC2
- **Fargate**: sin gestión de nodos, escala a 0 fuera de horario, pago por segundo.
- **EC2**: más barato a escala, pero requiere gestión del cluster y reserva de capacidad.
- Para un SaaS early-stage, Fargate elimina overhead operacional que no genera valor.

### CloudFront para el frontend
- 400+ edge locations en LATAM → latencia <50ms desde Colombia.
- SSL/TLS gratis con el certificado default de CloudFront.
- Next.js exportado como `output: "standalone"` → solo archivos estáticos, no requiere servidor Node.
- S3 + CloudFront cuesta ~$0.01/GB transferido vs $0.085/GB de EC2.

### RDS en subnet privada
- La base de datos nunca es accesible desde internet — solo ECS puede conectarse.
- `db.t4g.micro` (~$13/mes) es suficiente para un prototipo con < 1000 evaluaciones/día.

## Variables necesarias

```hcl
aws_region     = "us-east-1"
project_name   = "micpose"
environment    = "production"
db_password    = "<secreto>"       # usar AWS Secrets Manager en prod
openai_api_key = "sk-..."          # usar AWS Secrets Manager en prod
api_image_uri  = "123456789.dkr.ecr.us-east-1.amazonaws.com/micpose-api:latest"
```

## Cómo usar

```bash
terraform init
terraform plan -var-file=prod.tfvars
terraform apply -var-file=prod.tfvars
```
