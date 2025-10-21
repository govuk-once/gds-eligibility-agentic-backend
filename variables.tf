variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "eu-west-2"
}

variable "agent_name" {
  description = "Name of the Bedrock agent"
  type        = string
  default     = "gds_eligability_terraform_sandbox_eligability_agent"
}

variable "foundation_model" {
  description = "Foundation model for the agent"
  type        = string
  default     = "anthropic.claude-3-sonnet-20240229-v1:0"
}

variable "agent_instruction" {
  description = "Instructions for the agent"
  type        = string
  default     = "You are a helpful assistant. Who's a good assistant? You are! Yes, you are, yes you are"
}
