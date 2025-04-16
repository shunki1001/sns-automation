variable "iam_roles" {
  description = "サービスアカウントに付与する IAM ロールのリスト"
  type        = list(string)
  default     = [
    "roles/cloudtasks.enqueuer",
    "roles/iam.serviceAccountUser"
  ]
}
variable cloud_functions {}