output "agent_id" {
  description = "ID of the created Bedrock agent"
  value       = aws_bedrockagent_agent.example.agent_id
}

output "agent_arn" {
  description = "ARN of the created Bedrock agent"
  value       = aws_bedrockagent_agent.example.agent_arn
}
