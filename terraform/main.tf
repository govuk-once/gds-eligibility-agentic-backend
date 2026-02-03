terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 6.27.0"
    }
  }
  backend "s3" {}
}

provider "aws" {
  region = "eu-west-2"
}

resource "aws_s3_bucket" "eligibility_transcripts" {     
  count = terraform.workspace == "goe-staging" ? 1 : 0                                                                                                                                                                                                                                                                
  bucket = "gds-eligibility-transcripts-goe-staging"                                                                                                                                                                                                                                                          
}   