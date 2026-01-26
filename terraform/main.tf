terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.17"
    }
  }
  backend "s3" {}
}

provider "aws" {
  region = "eu-west-2"
}

resource "aws_s3_bucket" "eligibility_transcripts" {                                                                                                                                                                                                                                                                     
  bucket = "gds-eligibility-transcripts-goe-staging"                                                                                                                                                                                                                                                          
}   