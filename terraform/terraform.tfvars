cloud_functions = {
  x-post = {
    description = "Xへの投稿をする関数"
    source_dir  = "/functions/x-post"
    memory = "512Mi"
    timeout_seconds = "540"
    runtime = "python311"
  },
}