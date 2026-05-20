output "alb_dns_name" {
  description = "DNS del Application Load Balancer (apunta al API FastAPI)"
  value       = aws_alb.main.dns_name
}

output "cloudfront_domain" {
  description = "Dominio CloudFront para acceder al frontend"
  value       = aws_cloudfront_distribution.frontend.domain_name
}

output "rds_endpoint" {
  description = "Endpoint del RDS PostgreSQL (solo accesible desde subnet privada)"
  value       = aws_db_instance.main.address
}

output "audio_bucket_name" {
  description = "Nombre del bucket S3 para audios"
  value       = aws_s3_bucket.audio.bucket
}

output "frontend_bucket_name" {
  description = "Nombre del bucket S3 para assets del frontend"
  value       = aws_s3_bucket.frontend.bucket
}
