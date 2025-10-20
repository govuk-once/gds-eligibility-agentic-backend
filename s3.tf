resource "aws_s3_bucket" "knowledge_base" {
  bucket = "bedrock-agent-knowledge-base-${random_id.id.hex}"
}

resource "random_id" "id" {
  byte_length = 8
}
