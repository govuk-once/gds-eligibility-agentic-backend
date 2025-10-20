variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "agent_name" {
  description = "Name of the Bedrock agent"
  type        = string
  default     = "example-agent"
}

variable "foundation_model" {
  description = "Foundation model for the agent"
  type        = string
  default     = "anthropic.claude-3-sonnet-20240229-v1:0"
}

variable "agent_instruction" {
  description = "Instructions for the agent"
  type        = string
  default     = "You are a helpful assistant."
}
