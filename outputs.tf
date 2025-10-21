output "agent_id" {
  description = "ID of the created Bedrock agent"
  value       = aws_bedrockagent_agent.eligability_agent.agent_id
}

output "agent_arn" {
  description = "ARN of the created Bedrock agent"
  value       = aws_bedrockagent_agent.eligability_agent.agent_arn
}
