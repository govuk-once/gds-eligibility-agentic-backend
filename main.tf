provider "aws" {
  region = var.aws_region
}

resource "aws_bedrockagent_agent" "example" {
  agent_name = "example"
  foundation_model = "anthropic.claude-v2"
  agent_resource_role_arn = aws_iam_role.bedrock_agent_role.arn
  instruction = "You are a helpful assistant."
}

resource "aws_bedrockagent_knowledge_base" "example" {
  name = "example"
  role_arn = aws_iam_role.bedrock_agent_role.arn

  knowledge_base_configuration {
    type = "VECTOR"
    vector_knowledge_base_configuration {
      embedding_model_arn = "arn:aws:bedrock:${var.aws_region}::foundation-model/amazon.titan-embed-text-v1"
    }
  }

  storage_configuration {
    type = "S3"
    s3_configuration {
      bucket_arn = aws_s3_bucket.knowledge_base.arn
    }
  }
}

resource "aws_bedrockagent_agent_knowledge_base_association" "example" {
  agent_id = aws_bedrockagent_agent.example.id
  knowledge_base_id = aws_bedrockagent_knowledge_base.example.id
  description = "Example knowledge base association"
  knowledge_base_state = "ENABLED"
}
