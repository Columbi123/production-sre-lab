
terraform {
  backend "s3" {
    bucket = "sre-terraform-state-sofmishasof"
    key    = "production-sre-lab/terraform.tfstate"
    region = "ru-central1"

    endpoints = {
      s3 = "https://storage.mwsapis.ru"
    }

    skip_region_validation      = true
    skip_credentials_validation = true
    skip_metadata_api_check     = true
    skip_requesting_account_id  = true

    use_path_style         = true
    use_dualstack_endpoint = false
    use_fips_endpoint      = false
    use_lockfile           = false
  }
}
