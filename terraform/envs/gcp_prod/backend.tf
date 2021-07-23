terraform {
  backend "gcs" {
    bucket = "hkak03key-examples-prod-terraform"
    prefix = "tfstate"
  }
}

