variable "project_id" {
  description = "ID del proyecto en GCP"
  type        = string
  default     = "silicon-amulet-432102-s9"
}

variable "region" {
  description = "Región donde se desplegarán los recursos"
  type        = string
  default     = "us-central1"
}
