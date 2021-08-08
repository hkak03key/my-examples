module "google_cloudfunctions_printenv" {
  source = "../../modules/google_cloudfunctions_printenv"

  tf_bucket = local.tf_bucket
}
