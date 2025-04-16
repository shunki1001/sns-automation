terraform {
  backend "gcs" {
    bucket  = "terrform-bucket-smarthome-428311"
    prefix  = "state/sns-automation"
  }
}
provider "google" {
  project = "smarthome-428311"  # 使用するGCPプロジェクトID
  region  = "asia-northeast1"      # GCPリージョン（例：us-central1）
}
locals {
  project = "smarthome-428311"  # 使用するGCPプロジェクトID
  region  = "asia-northeast1" 
}


resource "google_service_account" "account" {
  account_id   = "sns-invoker"
  display_name = "sns-invoker"
}

resource "google_project_iam_member" "project" {
  for_each = toset(var.iam_roles)
  project = local.project
  role    = each.value
  member  = "serviceAccount:${google_service_account.account.email}"
}

resource "google_storage_bucket" "bucket" {
  name                        = "${local.project}-gcf-source"  # Every bucket name must be globally unique
  location                    = local.region
}

data "archive_file" "gcf-function" {
  for_each = var.cloud_functions
  type        = "zip"
  output_path = "./${each.key}/function-source.zip"
  source_dir    = "..${each.value.source_dir}"
  excludes    = ["env/**", "**/__pycache__/**","node_modules/**",] 
}

resource "google_storage_bucket_object" "object" {
  for_each = var.cloud_functions
  name   = "${each.key}/function_source_${substr(filemd5("./${each.key}/function-source.zip"), 0, 8)}.zip"
  bucket = google_storage_bucket.bucket.name
  source = "./${each.key}/function-source.zip"
}

resource "google_cloudfunctions2_function" "coupon_function" {
  for_each = var.cloud_functions
  name = each.key
  location = local.region
  description = each.value.description

  build_config {
    runtime = each.value.runtime
    entry_point = "main"  # Set the entry point 
    environment_variables = yamldecode(file("..${each.value.source_dir}/.env.yaml"))
    source {
      storage_source {
        bucket = google_storage_bucket.bucket.name
        object = google_storage_bucket_object.object[each.key].name
      }
    }
  }

  service_config {
    max_instance_count  = 1
    min_instance_count = 0
    available_memory    = each.value.memory
    timeout_seconds     = each.value.timeout_seconds
    service_account_email = google_service_account.account.email
  }
}

resource "google_cloudfunctions2_function_iam_member" "invoker" {
  for_each = var.cloud_functions
  project        = google_cloudfunctions2_function.coupon_function[each.key].project
  location       = google_cloudfunctions2_function.coupon_function[each.key].location
  cloud_function = google_cloudfunctions2_function.coupon_function[each.key].name
  role           = "roles/cloudfunctions.invoker"
  member         = "serviceAccount:${google_service_account.account.email}"
}

resource "google_cloud_run_service_iam_member" "cloud_run_invoker" {
  for_each = var.cloud_functions
  project  = google_cloudfunctions2_function.coupon_function[each.key].project
  location = google_cloudfunctions2_function.coupon_function[each.key].location
  service  = google_cloudfunctions2_function.coupon_function[each.key].name
  role     = "roles/run.invoker"
  member   = "serviceAccount:${google_service_account.account.email}"
}





resource "google_cloud_tasks_queue" "http_target_oidc" {
   name     = "cloud-tasks-x-post"
   location = local.region
 
   http_target {
     http_method = "POST"
     oidc_token {
       audience              = "${google_cloudfunctions2_function.coupon_function["x-post"].service_config[0].uri}/"
       service_account_email = google_service_account.account.email
     }
   }
 }