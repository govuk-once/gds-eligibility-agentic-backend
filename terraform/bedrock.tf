locals {
  model_id = "anthropic.claude-3-7-sonnet-20250219-v1:0"
  system_instruction = file("../prompts/agents/Prompt_Draft_Eligibility.md")
}

resource "aws_iam_role" "bedrock_agent_role" {
  name = "bedrock-agent-role-${terraform.workspace}"

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

resource "aws_iam_role" "bedrock_execution_role" {
  name = "bedrock-execution-role-${terraform.workspace}"

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

resource "aws_iam_role_policy" "bedrock_execution_policy" {
  name = "bedrock-execution-policy-${terraform.workspace}"
  role = aws_iam_role.bedrock_execution_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "bedrock:InvokeAgent"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "bedrock_execution_policy_limited_access" {
  role       = aws_iam_role.bedrock_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonBedrockFullAccess"
}

resource "aws_iam_role_policy_attachment" "bedrock_agent_policy_limited_access" {
  role       = aws_iam_role.bedrock_agent_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonBedrockFullAccess"
}

resource "aws_bedrockagent_agent" "eligability_agent" {
  agent_name              = "gds_eligability_terraform_sandbox_eligability_agent-${terraform.workspace}"
  agent_resource_role_arn = aws_iam_role.bedrock_agent_role.arn
  foundation_model        = local.model_id
  instruction             = local.system_instruction
}

# # This doesn't actually work as descibed by the terraform documentation, and generates errononeous conflicts
# # See https://github.com/hashicorp/terraform-provider-aws/issues/43045
# # resource "aws_bedrockagent_agent_action_group" "allow_user_input" {
# #     action_group_name = "allow_user_input"
# #     agent_id = aws_bedrockagent_agent.eligability_agent.id
# #     agent_version = "DRAFT"
# #     parent_action_group_signature = "AMAZON.UserInput"
# }

resource "aws_bedrockagent_agent_alias" "eligability_alias_for_prompts" {
  agent_alias_name = "eligability-alias-for-prompts-${terraform.workspace}"
  agent_id         = aws_bedrockagent_agent.eligability_agent.agent_id
  description      = "Alias to allow linkage between eligability agent and prompts"
}

# resource "aws_bedrockagent_prompt" "triage_prompt" {
#   name            = "triage_prompt_${terraform.workspace}"
#   description     = "This is an entrypoint prompt to triage the users initial input"
#   default_variant = "triage_variant"


#   variant {
#     name          = "triage_variant"
#     model_id      = local.model_id
#     template_type = "CHAT"

#     inference_configuration {
#       text {
#         max_tokens     = 2048
#         stop_sequences = ["User:"]
#         temperature    = 0
#         top_p          = 0.8999999761581421
#       }
#     }

#     template_configuration {
#       chat {
#         system {
#           text = local.system_instruction
#         }
#         message {
#           role = "user"
#           content {
#             text = "{{user_input}}"
#           }
#         }
#         input_variable {
#           name = "user_input"
#         }
#       }
#     }
#     # gen_ai_resource {
#     #   agent {
#     #     agent_identifier = aws_bedrockagent_agent_alias.eligability_alias_for_prompts.agent_alias_arn
#     #   }
#     # }
#   }
# }

resource "aws_bedrockagent_flow" "triage" {
  name               = "triage-flow-${terraform.workspace}"
  execution_role_arn = aws_iam_role.bedrock_execution_role.arn
  # TODO would this be better composed as a set of data blocks? Could they be made resusable somehow?
  definition {
    connection {
      name   = "FlowInputNodeFlowInputNode0ToAgent_1PromptsNode0"
      source = "FlowInputNode"
      target = "Triage"
      type   = "Data"
      configuration {
        data {
          source_output = "document"
          target_input  = "agentInputText"
          # target_input  = "user_input"
        }
      }
    }

    connection {
      name   = "Agent_1PromptsNode0ToFlowOutputNodeFlowOutputNode0"
      source = "Triage"
      target = "FlowOutputNode"
      type   = "Data"
      configuration {
        data {
          source_output = "agentResponse"
          # source_output = "modelCompletion"
          target_input  = "document"
        }
      }
    }

    node {
      name = "FlowInputNode"
      type = "Input"
      configuration {
        input {}
      }
      output {
        name = "document"
        type = "String"
      }
    }

    # node {
    #   name = "Triage"
    #   type = "Prompt"
    #   configuration {
    #     prompt {
    #       source_configuration {
    #         resource {
    #           prompt_arn = aws_bedrockagent_prompt.triage_prompt.arn
    #         }
    #       }
    #     }
    #   }
    #   input {
    #     expression = "$.data"
    #     name       = "user_input"
    #     type       = "String"
    #   }
    #   output {
    #     name       = "modelCompletion"
    #     type       = "String"
    #   }
    # }

    node {
      name = "Triage"
      type = "Agent"
      configuration {
        agent {
          agent_alias_arn = aws_bedrockagent_agent_alias.eligability_alias_for_prompts.agent_alias_arn
        }
      }
      input {
        expression = "$.data"
        name       = "agentInputText"
        type       = "String"
      }
      input {
        expression = "$.data"
        name       = "promptAttributes"
        type       = "Object"
      }
      input {
        expression = "$.data"
        name       = "sessionAttributes"
        type       = "Object"
      }
      output {
        name = "agentResponse"
        type = "String"
      }
    }

    node {
      name = "FlowOutputNode"
      type = "Output"
      configuration {
        output {}
      }
      input {
        expression = "$.data"
        name       = "document"
        type       = "String"
      }
    }
  }
}
