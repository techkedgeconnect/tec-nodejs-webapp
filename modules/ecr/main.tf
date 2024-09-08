resource "aws_ecr_repository" "tec-ecr-repo" {
  for_each             = toset(var.aws_ecr_name)
  name                 = each.key
  image_tag_mutability = var.image_mutability
  encryption_configuration {
    encryption_type = var.encrypt_type
  }
  image_scanning_configuration {
    scan_on_push = true
  }
  tags = var.tags
}
