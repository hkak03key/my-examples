terraform {
  backend "gcs" {
    bucket = "hkak03key-samples-prod-terraform"
    prefix = "tfstate"
  }
}

