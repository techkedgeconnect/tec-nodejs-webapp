output "ecr_repository_urls" {
  description = "The URLs of the ECR repositories"
  value       = { for repo_name, repo in aws_ecr_repository.tec-ecr-repo : repo_name => repo.repository_url }
}

output "ecr_repository_arns" {
  description = "The ARNs of the ECR repositories"
  value       = { for repo_name, repo in aws_ecr_repository.tec-ecr-repo : repo_name => repo.arn }
}

output "ecr_repository_names" {
  description = "The names of the ECR repositories"
  value       = { for repo_name, repo in aws_ecr_repository.tec-ecr-repo : repo_name => repo.name }
}
