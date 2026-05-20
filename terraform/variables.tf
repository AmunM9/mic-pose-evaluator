variable "aws_region" {
  description = "AWS region where all resources will be deployed"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Base name used to prefix all resource names"
  type        = string
  default     = "micpose"
}

variable "environment" {
  description = "Deployment environment: staging or production"
  type        = string
  default     = "production"
  validation {
    condition     = contains(["staging", "production"], var.environment)
    error_message = "Must be 'staging' or 'production'."
  }
}

variable "db_password" {
  description = "Master password for the RDS PostgreSQL instance"
  type        = string
  sensitive   = true
}

variable "openai_api_key" {
  description = "OpenAI API key injected into ECS task as environment variable"
  type        = string
  sensitive   = true
}

variable "api_image_uri" {
  description = "Docker image URI for the FastAPI backend (ECR or Docker Hub)"
  type        = string
}
