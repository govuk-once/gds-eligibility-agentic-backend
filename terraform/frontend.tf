locals {
  app_ecr_repo_name = "gds-eligability-frontend-repo"
  account_id   = data.aws_caller_identity.current.account_id
}

data "aws_caller_identity" "current" {}

resource "aws_ecr_repository" "frontend_app" {
  name = local.app_ecr_repo_name
}

resource "aws_apprunner_service" "frontend_app" {
  service_name = "gds-eligability-frontend-app"

  source_configuration {
    authentication_configuration {
      access_role_arn = aws_iam_role.frontend_app_ecr.arn
    }
    image_repository {
      # image_identifier      = data.aws_ecr_image.frontend_app.image_uri
      # Hardcode image to remove dependency loop imposed by image management being handled outside of terraform
      image_identifier      = "${local.account_id}.dkr.ecr.eu-west-2.amazonaws.com/gds-eligability-frontend-repo:latest"
      image_repository_type = "ECR"
      image_configuration {
        port = 3000
        runtime_environment_variables = {
          AWS_REGION                 = "eu-west-2"
          PINO_LOG_LEVEL             = "debug"
          PUBLIC_ADK_API_URL         = "https://${aws_apprunner_service.adk_server.service_url}"
          ADK_APP_NAME               = "sequential_agent"
          PROACTIVE_ADK_APP_NAME     = "userTesting3"
          CHILD_BENEFIT_ADK_APP_NAME = "gds_eligibility"
          ADK_USER_ID                = "user"
        }
        runtime_environment_secrets = {
          AUTH_USERNAME              = aws_ssm_parameter.frontend_username.arn
          AUTH_PASSWORD              = aws_ssm_parameter.frontend_password.arn
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
      is_publicly_accessible = true
    }
    egress_configuration {
      egress_type       = "VPC"
      vpc_connector_arn = aws_apprunner_vpc_connector.frontend_egress_connector.arn
    }
  }
  health_check_configuration {
    protocol = "HTTP"
    path     = "/health"
  }
}

resource "aws_ssm_parameter" "frontend_password" {
  name        = "/frontend/apprunner/env/AUTH_PASSWORD"
  description = "Password for basic auth on the frontend"
  type        = "SecureString"
  key_id      = aws_kms_key.ssm_aws_custom.arn
  value       = "CHANGEME"
  overwrite   = false
}

resource "aws_ssm_parameter" "frontend_username" {
  name        = "/frontend/apprunner/env/AUTH_USERNAME"
  description = "Username for basic auth on the frontend"
  type        = "SecureString"
  key_id      = aws_kms_key.ssm_aws_custom.arn
  value       = "CHANGEME"
  overwrite   = false
}

resource "aws_kms_key" "ssm_aws_custom" {
  description             = "Key for securing (frontend) service credentials"
  enable_key_rotation     = true
  deletion_window_in_days = 20
  policy = jsonencode({
    Version = "2012-10-17"
    Id      = "key-default-1"
    Statement = [
      {
        Sid    = "Enable IAM User Permissions"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        },
        Action   = "kms:*"
        Resource = "*"
      },
      {
        Sid    = "Allow use of the key"
        Effect = "Allow"
        Principal = {
          AWS = aws_iam_role.frontend_app_service.arn
        },
        Action = [
          "kms:DescribeKey",
          "kms:List*",
          "kms:Get*",
          "kms:Decrypt",
        ],
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role" "frontend_app_service" {
  name = "gds-eligability-frontend-app-service"
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
  name = "gds-eligability-frontend-app-ecr"
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
  role       = aws_iam_role.frontend_app_ecr.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSAppRunnerServicePolicyForECRAccess"
}

resource "aws_iam_role_policy_attachment" "frontend_app_service_apprunner" {
  role       = aws_iam_role.frontend_app_service.name
  policy_arn = "arn:aws:iam::aws:policy/AWSAppRunnerFullAccess"
}

resource "aws_iam_role_policy_attachment" "frontend_app_service_ssm_parameterstore_key" {
  role       = aws_iam_role.frontend_app_service.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMReadOnlyAccess"
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


