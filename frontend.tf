locals {
  ecr_repo_name = "gds-eligability-frontend-repo"
}

resource "aws_ecr_repository" "frontend_app" {
  count = terraform.workspace == "stable" ? 1 : 0
  name  = local.ecr_repo_name
}

# Both stable and unstable share the same ecr repo, use this accessor instead of the resource
# to make sure the reference is always valid
data "aws_ecr_repository" "frontend_app" {
  name  = local.ecr_repo_name
}


