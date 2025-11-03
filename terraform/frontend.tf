locals {
  ecr_repo_name = "gds-eligability-frontend-repo"
}

resource "aws_ecr_repository" "frontend_app" {
  count = terraform.workspace == "stable" ? 1 : 0
  name  = local.ecr_repo_name
}

# # Both stable and unstable share the same ecr repo, use this accessor instead of the resource
# # to make sure the reference is always valid
# data "aws_ecr_image" "frontend_app" {
#   repository_name = local.ecr_repo_name
#   image_tag       = terraform.workspace
# }

resource "aws_apprunner_service" "frontend_app" {
  service_name = "gds-eligability-frontend-app-${terraform.workspace}"

  source_configuration {
    authentication_configuration {
      access_role_arn = aws_iam_role.frontend_app_ecr.arn
    }
    image_repository {
      # image_identifier      = data.aws_ecr_image.frontend_app.image_uri
      # Hardcode image to remove dependency loop imposed by image management being handled outside of terraform
      image_identifier      = "261219435789.dkr.ecr.eu-west-2.amazonaws.com/gds-eligability-frontend-repo:${terraform.workspace}"
      image_repository_type = "ECR"
      image_configuration {
        runtime_environment_variables = {
          AWS_REGION = "eu-west-2"
          # Both the stable and unstable frontend will point to the stable flow
          # Can't use data source for aws_bedrockagent_flow, so have to hard code it
          BEDROCK_FLOW_ID = "RU8U3PTJF8" # aws_bedrockagent_flow.triage.id for workspace=stable
          # THis alias needs to be created manually!
          BEDROCK_FLOW_ALIAS_ID = "XC4VHFA93K"
          NODE_ENV = "production"
          PINO_LOG_LEVEL = "debug"
        }
      }
    }
    auto_deployments_enabled = true
  }
  instance_configuration {
    instance_role_arn = aws_iam_role.frontend_app_service.arn
  }
  network_configuration {
    ingress_configuration {
      is_publicly_accessible = false
    }
  }
  health_check_configuration {
    protocol = "HTTP"
    path     = "/health"
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
          Service = "tasks.apprunner.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role" "frontend_app_ecr" {
  name = "gds-eligability-frontend-app-ecr-${terraform.workspace}"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "build.apprunner.amazonaws.com"
        }
      }
    ]
  })
}


resource "aws_iam_role_policy_attachment" "frontend_app_ecr_role_ecr" {
  role = aws_iam_role.frontend_app_ecr.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSAppRunnerServicePolicyForECRAccess"
}

resource "aws_iam_role_policy_attachment" "frontend_app_service_apprunner" {
  role = aws_iam_role.frontend_app_service.name
  policy_arn = "arn:aws:iam::aws:policy/AWSAppRunnerFullAccess"
}

resource "aws_iam_role_policy" "frontend_app_service_bedrock" {
  role = aws_iam_role.frontend_app_service.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "bedrock:InvokeFlow"
        ]
        Resource = "*"
      }
    ]
  })
}


