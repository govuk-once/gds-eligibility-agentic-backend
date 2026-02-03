resource "aws_iam_role" "bedrock_kb_role" {
  name = "bedrock-knowledge-base-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = { Service = "bedrock.amazonaws.com" }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "bedrock_kb_policy" {
  name = "bedrock-kb-policy"
  role = aws_iam_role.bedrock_kb_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          # Redshift Serverless
          "redshift-data:ExecuteStatement",
          "redshift-data:DescribeStatement",
          "redshift-data:GetStatementResult",
          "redshift-serverless:GetWorkgroup",
          "redshift-serverless:GetNamespace",
          "redshift-serverless:ListDatabases",
          "redshift-serverless:GetDatabase",
          "redshift-serverless:*",
          "redshift-data:*",
          # Secrets for auto-managed password
          "secretsmanager:GetSecretValue",
          # Required by Bedrock KB
          "bedrock:GenerateQuery",
          "sqlworkbench:GetSqlRecommendations",
          "sqlworkbench:CreateSqlGenerationContext",
          "sqlworkbench:DeleteSqlGenerationContext",
          "sqlworkbench:PutSqlGenerationContext"
        ],
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role" "bedrock_agent_role" {
  name = "bedrock-agent-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = { Service = "bedrock.amazonaws.com" }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "bedrock_agent_policy" {
  name = "bedrock-agent-policy"
  role = aws_iam_role.bedrock_agent_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "bedrock:InvokeModel",
          "bedrock:GetKnowledgeBase",
          "bedrock:Retrieve",
          "bedrock:RetrieveAndGenerate"
        ],
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "bedrock_kb_redshift_access" {
  role       = aws_iam_role.bedrock_kb_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonRedshiftDataFullAccess"
}
  