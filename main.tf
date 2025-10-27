terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.17"
    }
  }
}

provider "aws" {
  region = "eu-west-2"
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
  policy_arn = "arn:aws:iam::aws:policy/AmazonBedrockLimitedAccess"
}

resource "aws_iam_role_policy_attachment" "bedrock_agent_policy_limited_access" {
  role       = aws_iam_role.bedrock_agent_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonBedrockLimitedAccess"
  # policy_arn = "arn:aws:iam::aws:policy/AmazonBedrockMarketplaceAccess"
  # policy_arn = "arn:aws:iam::aws:policy/AWSMarketplaceRead-only"
}

resource "aws_bedrockagent_agent" "eligability_agent" {
  agent_name              = "gds_eligability_terraform_sandbox_eligability_agent-${terraform.workspace}"
  agent_resource_role_arn = aws_iam_role.bedrock_agent_role.arn
  foundation_model        = "amazon.nova-lite-v1:0"
  instruction             = var.agent_instruction
}

# This doesn't actually work as descibed by the terraform documentation, and generates errononeous conflicts
# See https://github.com/hashicorp/terraform-provider-aws/issues/43045
# resource "aws_bedrockagent_agent_action_group" "allow_user_input" {
#     action_group_name = "allow_user_input"
#     agent_id = aws_bedrockagent_agent.eligability_agent.id
#     agent_version = "DRAFT"
#     parent_action_group_signature = "AMAZON.UserInput"
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
#     template_type = "TEXT"

#     inference_configuration {
#       text {
#         max_tokens     = 2048
#         stop_sequences = ["User:"]
#         temperature    = 0
#         top_p          = 0.8999999761581421
#       }
#     }

#     template_configuration {
#       text {
#         text = "Write a paragraph about {{topic}}."

#         input_variable {
#           name = "topic"
#         }
#       }
#     }
#     gen_ai_resource {
#       agent {
#         agent_identifier = aws_bedrockagent_agent_alias.eligability_alias_for_prompts.agent_alias_arn
#       }
#     }
#   }
# }

resource "aws_s3_bucket" "dialogue_storage" {
  bucket = "gds-eligability-dialogue-storage-${terraform.workspace}"
}

resource "aws_s3_bucket_public_access_block" "dialogue_storage" {
  bucket = aws_s3_bucket.dialogue_storage.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

module "recall_for_user" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "recall_for_user-${terraform.workspace}"
  description   = "Recall past user interactions with agent"
  handler       = "main.lambda_handler"
  runtime       = "python3.12"

  source_path = "./src/lambda/recall_for_user"

}

resource "aws_bedrockagent_flow" "triage" {
  name               = "triage-flow-${terraform.workspace}"
  execution_role_arn = aws_iam_role.bedrock_execution_role.arn
  # TODO would this be better composed as a set of data blocks? Could they be made resusable somehow?
  definition {
    connection {
      name   = "FlowInputNodeFlowInputNode0ToAgent_1PromptsNode0"
      source = "FlowInputNode"
      target = "Agent_1"
      type   = "Data"
      configuration {
        data {
          source_output = "document"
          target_input  = "agentInputText"
        }
      }
    }

    # connection {
    #   name   = "FlowInputNodeToRecallForUsercodeHookInput"
    #   source = "FlowInputNode"
    #   target = "RecallForUser"
    #   type   = "Data"
    #   configuration {
    #     data {
    #       source_output = "document"
    #       target_input  = "codeHookInput"
    #     }
    #   }
    # }

    # connection {
    #   name   = "RecallForUserToAgent_1SessionAttributes"
    #   source = "RecallForUser"
    #   target = "Agent_1"
    #   type   = "Data"
    #   configuration {
    #     data {
    #       source_output = "functionResponse"
    #       target_input  = "sessionAttributes"
    #     }
    #   }
    # }

    # connection {
    #   name   = "Agent_1agentResponseToStoreDialoguecontent"
    #   source = "Agent_1"
    #   target = "StoreDialogue"
    #   type   = "Data"
    #   configuration {
    #     data {
    #       source_output = "agentResponse"
    #       target_input  = "content"
    #     }
    #   }
    # }

    # connection {
    #   name   = "RecallForUserfunctionReponseToStoreDialogueobjectKey"
    #   source = "RecallForUser"
    #   target = "StoreDialogue"
    #   type   = "Data"
    #   configuration {
    #     data {
    #       source_output = "functionResponse"
    #       target_input  = "objectKey"
    #     }
    #   }
    # }
    connection {
      name   = "Agent_1PromptsNode0ToFlowOutputNodeFlowOutputNode0"
      source = "Agent_1"
      target = "FlowOutputNode"
      type   = "Data"
      configuration {
        data {
          source_output = "agentResponse"
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
        type = "Object"
      }
    }

    # node {
    #   name = "RecallForUser"
    #   type = "LambdaFunction"
    #   configuration {
    #     lambda_function {
    #       lambda_arn = module.recall_for_user.lambda_function_arn
    #     }
    #   }
    #   input {
    #     expression = "$.data.userId"
    #     name       = "codeHookInput"
    #     type       = "String" # TODO this probably wants to be an object?
    #   }
    #   output {
    #     name = "functionResponse"
    #     type = "Object"
    #   }
    # }

    node {
      name = "Agent_1"
      type = "Agent"
      configuration {
        agent {
          agent_alias_arn = aws_bedrockagent_agent_alias.eligability_alias_for_prompts.agent_alias_arn
        }
      }
      input {
        # expression = "$.data.inputString"
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

    # node {
    #   name = "StoreDialogue"
    #   type = "Storage"
    #   configuration {
    #     storage {
    #       service_configuration {
    #         s3 {
    #           bucket_name = aws_s3_bucket.dialogue_storage.bucket
    #         }
    #       }
    #     }
    #   }
    #   input {
    #     expression = "$.data"
    #     name       = "content"
    #     type       = "String"
    #   }
    #   input {
    #     expression = "$.data.newStorageKey"
    #     name       = "objectKey"
    #     type       = "String"
    #   }
    #   output {
    #     name       = "s3Uri"
    #     type       = "String"
    #   }
    # }

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

