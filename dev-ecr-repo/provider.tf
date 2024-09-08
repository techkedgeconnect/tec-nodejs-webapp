# Define cloud provider block
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Configure the AWS Provider with input variable
provider "aws" {
  region = var.aws_region
}
