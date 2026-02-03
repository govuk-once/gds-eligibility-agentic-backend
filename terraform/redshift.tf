# terraform/redshift.tf

resource "aws_redshiftserverless_namespace" "bedrock_kb" {
  namespace_name       = "bedrock-kb"
  db_name              = "eligibility"
  admin_username       = "adminuser"
  manage_admin_password = true
}

resource "aws_redshiftserverless_workgroup" "bedrock_kb" {
  workgroup_name = "bedrock-kb"
  namespace_name = aws_redshiftserverless_namespace.bedrock_kb.namespace_name
}
