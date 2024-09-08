module "ecr-repo" {
  source           = "./../modules/ecr"
  aws_ecr_name     = var.aws_ecr_name
  tags             = var.tags
  image_mutability = var.image_mutability

}
