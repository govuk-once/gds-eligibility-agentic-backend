terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.17"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_iam_role" "bedrock_agent_role" {
  name = "bedrock-agent-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "bedrock.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "bedrock_agent_policy" {
  name = "bedrock-agent-policy"
  role = aws_iam_role.bedrock_agent_role.id

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

resource "aws_bedrockagent_agent" "eligability_agent" {
  agent_name              = var.agent_name
  agent_resource_role_arn = aws_iam_role.bedrock_agent_role.arn
  foundation_model        = var.foundation_model
  instruction             = var.agent_instruction
}
resource "aws_bedrockagent_agent_action_group" "allow_user_input" {
    action_group_name = "allow_user_input"
    agent_id = aws_bedrockagent_agent.eligability_agent.id
    agent_version = "DRAFT"
    parent_action_group_signature = "AMAZON.UserInput"
}
