data "aws_region" "this" {}

data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default_vpc_default_subnets" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

data "aws_security_groups" "default_vpc" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

resource "aws_apprunner_vpc_connector" "frontend_egress_connector" {
  vpc_connector_name = "frontend-apprunner-egress"
  subnets            = data.aws_subnets.default_vpc_default_subnets.ids
  security_groups    = data.aws_security_groups.default_vpc.ids
}

resource "aws_vpc_endpoint" "adk_ingress_connection" {
  vpc_id            = data.aws_vpc.default.id
  service_name      = "com.amazonaws.${data.aws_region.this.name}.apprunner.requests"
  vpc_endpoint_type = "Interface"
  subnet_ids        = data.aws_subnets.default_vpc_default_subnets.ids
}

resource "aws_apprunner_vpc_ingress_connection" "adk_ingress_connection" {
  name        = "adk_ingress_connection"
  service_arn = aws_apprunner_service.adk_server.arn

  ingress_vpc_configuration {
    vpc_id          = data.aws_vpc.default.id
    vpc_endpoint_id = aws_vpc_endpoint.adk_ingress_connection.id
  }
}


