locals {
  adk_ecr_repo_name = "gds-eligability-adk-repo"
}

resource "aws_ecr_repository" "adk_server" {
  count = terraform.workspace == "stable" ? 1 : 0
  name  = local.adk_ecr_repo_name
}

resource "aws_apprunner_service" "adk_server" {
  service_name = "gds-eligability-adk-server-${terraform.workspace}"

  source_configuration {
    authentication_configuration {
      access_role_arn = aws_iam_role.frontend_app_ecr.arn
    }
    image_repository {
      # Hardcode image to remove dependency loop imposed by image management being handled outside of terraform
      image_identifier      = "${local.account_id}.dkr.ecr.eu-west-2.amazonaws.com/gds-eligability-adk-repo:${terraform.workspace}"
      image_repository_type = "ECR"
      image_configuration {
        runtime_environment_variables = {
          PROMPTS_DIR = "/prompts"
        }
        port = 8000
      }
    }
    auto_deployments_enabled = true
  }
  instance_configuration {
    instance_role_arn = aws_iam_role.adk_app_service.arn
  }
  network_configuration {
    ingress_configuration {
      is_publicly_accessible = true
    }
  }
  health_check_configuration {
    protocol = "HTTP"
    path     = "/dev-ui/assets/config/runtime-config.json"

  }
}

resource "aws_iam_role" "adk_app_service" {
  name = "gds-eligability-adk-app-service-${terraform.workspace}"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "tasks.apprunner.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "adk_app_service_apprunner" {
  role       = aws_iam_role.adk_app_service.name
  policy_arn = "arn:aws:iam::aws:policy/AWSAppRunnerFullAccess"
}

resource "aws_iam_role_policy" "adk_app_service_bedrock" {
  role = aws_iam_role.adk_app_service.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "bedrock:InvokeModel"
        ]
        Resource = "*"
      }
    ]
  })
}


