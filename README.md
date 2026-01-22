## Terraform Deployment
1. `cd terraform`
2. `aws-vault exec govuk-once-eligibility-staging -- terraform init -backend-config=./staging.s3.tfbackend -reconfigure`
3. `aws-vault exec govuk-once-eligibility-staging -- terraform workspace select goe-staging`
4. `aws-vault exec govuk-once-eligibility-staging -- terraform plan`
5. `aws-vault exec govuk-once-eligibility-staging -- terraform apply`


## Local development
1. `aws-vault exec govuk-once-eligibility-staging -- docker-compose up`