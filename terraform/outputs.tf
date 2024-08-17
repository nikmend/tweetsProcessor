output "q1_memory_function_url" {
  description = "The URL to invoke the function q1_memory"
  value       = google_cloudfunctions_function.q1_memory_function.https_trigger_url
}

output "q1_time_function_url" {
  description = "Process any remaining tweets in the buffer"
  value       = google_cloudfunctions_function.q1_time_function.https_trigger_url
}
