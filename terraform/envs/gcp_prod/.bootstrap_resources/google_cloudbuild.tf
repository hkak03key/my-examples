module "google_cloudbuild_tf_plan_for_pr" {
  source                     = "../../../modules/google_cloudbuild_terraform"
  name                       = "tf-plan-for-pr"
  terraform_docker_image_ver = "1.0.2"
  terraform_check_fmt_dir    = "terraform"
  terraform_exec_dir         = "terraform/envs/gcp_prod"
  github = {
    owner = "hkak03key"
    name  = "my-examples"
    pull_request = {
      branch = ".*"
    }
  }
  proc = "plan"

  depends_on = [
    google_project_service.services,
  ]
}

module "google_cloudbuild_tf_apply_main_branch" {
  source                     = "../../../modules/google_cloudbuild_terraform"
  name                       = "tf-apply-main-branch"
  terraform_docker_image_ver = "1.0.2"
  terraform_check_fmt_dir    = "terraform"
  terraform_exec_dir         = "terraform/envs/gcp_prod"
  github = {
    owner = "hkak03key"
    name  = "my-examples"
    push = {
      branch = "^main$"
    }
  }
  proc = "apply"

  depends_on = [
    google_project_service.services,
  ]
}


