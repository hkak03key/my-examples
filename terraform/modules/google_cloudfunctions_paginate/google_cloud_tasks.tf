resource "google_cloud_tasks_queue" "this" {
  name     = local.module_name
  location = local.region

  rate_limits {
    max_concurrent_dispatches = 1
  }
}
