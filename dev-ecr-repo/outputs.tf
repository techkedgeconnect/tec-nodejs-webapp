output "ecr_repository_urls" {
  description = "The URLs of the ECR repositories from the ecr-repo module"
  value       = module.ecr-repo.ecr_repository_urls
}

output "ecr_repository_arns" {
  description = "The ARNs of the ECR repositories from the ecr-repo module"
  value       = module.ecr-repo.ecr_repository_arns
}

output "ecr_repository_names" {
  description = "The names of the ECR repositories from the ecr-repo module"
  value       = module.ecr-repo.ecr_repository_names
}
