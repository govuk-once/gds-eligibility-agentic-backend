locals {
  ecr_repo_name = "gds-eligability-frontend-repo"
}

resource "aws_ecr_repository" "frontend_app" {
  count = terraform.workspace == "stable" ? 1 : 0
  name  = local.ecr_repo_name
}

# Both stable and unstable share the same ecr repo, use this accessor instead of the resource
# to make sure the reference is always valid
data "aws_ecr_image" "frontend_app" {
  repository_name = local.ecr_repo_name
  image_tag       = terraform.workspace
}

resource "aws_apprunner_service" "frontend_app" {
  service_name = "gds-eligability-frontend-app-${terraform.workspace}"

  source_configuration {
    authentication_configuration {
      access_role_arn = aws_iam_role.frontend_app_service.arn
    }
    image_repository {
      image_identifier      = data.aws_ecr_image.frontend_app.image_uri
      image_repository_type = "ECR"
    }
    auto_deployments_enabled = true
  }
  network_configuration {
    ingress_configuration {
      is_publicly_accessible = false
    }
  }
}

resource "aws_iam_role" "frontend_app_service" {
  name = "gds-eligability-frontend-app-service-${terraform.workspace}"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "apprunner.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "frontend_app_service_ecr" {
  role = aws_iam_role.frontend_app_service.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSAppRunnerServicePolicyForECRAccess"
}

resource "aws_iam_role_policy_attachment" "frontend_app_service_apprunner" {
  role = aws_iam_role.frontend_app_service.name
  policy_arn = "arn:aws:iam::aws:policy/AWSAppRunnerFullAccess"
}
