###################################################
# script upload to gcs

#---------------
# zip on local
data "archive_file" "gcf_codes" {
  for_each = toset(
    [
      # TODO: enum to upload dir
      "scripts/printenv",
    ]
  )

  type        = "zip"
  source_dir  = "${path.module}/${each.value}"
  output_path = "${path.module}/.temp/${each.value}.zip"
}

#---------------
# upload
resource "google_storage_bucket_object" "gcf_codes" {
  for_each = {
    for v in keys(data.archive_file.gcf_codes)
    : v => data.archive_file.gcf_codes[v]
  }
  name   = "${local.module_name}/gcf/${each.key}/${each.value.output_md5}.zip"
  bucket = var.tf_bucket
  source = each.value.output_path
}

###################################################
# each function

#======================
## this

#---------------
### function
resource "google_cloudfunctions_function" "this" {
  name        = replace(local.module_name, "/", "-")
  description = local.module_name
  runtime     = "python39"

  available_memory_mb   = 128
  service_account_email = google_service_account.this.email
  source_archive_bucket = google_storage_bucket_object.gcf_codes["scripts/printenv"].bucket
  source_archive_object = google_storage_bucket_object.gcf_codes["scripts/printenv"].name
  trigger_http          = true
  entry_point           = "main"
}

#---------------
# invoker
resource "google_cloudfunctions_function_iam_binding" "this" {
  project        = google_cloudfunctions_function.this.project
  region         = google_cloudfunctions_function.this.region
  cloud_function = google_cloudfunctions_function.this.name

  role = "roles/cloudfunctions.invoker"
  members = [
    # TODO: enum invokers
  ]

  depends_on = [
    google_cloudfunctions_function.this,
  ]
}

