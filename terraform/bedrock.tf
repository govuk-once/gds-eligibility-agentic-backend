resource "aws_bedrockagent_knowledge_base" "structured" {
  name     = "eligibility-structured-kb"
  role_arn = aws_iam_role.bedrock_kb_role.arn

  knowledge_base_configuration {
    type = "SQL"

    sql_knowledge_base_configuration {
      type = "REDSHIFT"

      redshift_configuration {
        query_engine_configuration {
          type = "SERVERLESS"

          serverless_configuration {
            workgroup_arn = aws_redshiftserverless_workgroup.bedrock_kb.arn

            auth_configuration {
              type                         = "USERNAME_PASSWORD"
              username_password_secret_arn = aws_redshiftserverless_namespace.bedrock_kb.admin_password_secret_arn
            }
          }
        }

        storage_configuration {
          type = "REDSHIFT"

          redshift_configuration {
            database_name = aws_redshiftserverless_namespace.bedrock_kb.db_name
          }
        }
      }
    }
  }
}

resource "aws_bedrockagent_agent" "eligibility" {
  agent_name                = "eligibility-agent"
  foundation_model          = var.bedrock_agent_foundation_model
  instruction               = "You are a helpful agent that can answer questions about user eligibility for government services."
  agent_resource_role_arn   = aws_iam_role.bedrock_agent_role.arn
}

resource "aws_bedrockagent_agent_knowledge_base_association" "eligibility_kb_association" {
  agent_id             = aws_bedrockagent_agent.eligibility.id
  knowledge_base_id    = aws_bedrockagent_knowledge_base.structured.id
  knowledge_base_state = "ENABLED"
  description          = "The knowledge base containing user eligibility information."
}