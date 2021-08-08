resource "google_project_service" "services" {
  for_each = toset([
    "calendar-json.googleapis.com",
    "cloudfunctions.googleapis.com",
    "cloudscheduler.googleapis.com",
    "cloudtasks.googleapis.com",
    "iam.googleapis.com",
    "sheets.googleapis.com",
  ])

  project                    = local.project_id
  service                    = each.value
  disable_dependent_services = true
}

