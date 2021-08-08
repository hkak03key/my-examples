module "google_cloudfunctions_printenv" {
  source = "../../modules/google_cloudfunctions_printenv"

  tf_bucket = local.tf_bucket

  depends_on = [
    google_project_service.services,
  ]
}

module "google_cloudfunctions_paginate" {
  source = "../../modules/google_cloudfunctions_paginate"

  tf_bucket = local.tf_bucket

  depends_on = [
    google_project_service.services,
  ]
}
