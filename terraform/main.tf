provider "google" {
  project = var.project_id
  region  = var.region
}

# Creación del bucket de GCS
resource "google_storage_bucket" "data_bucket" {
  name     = "${var.project_id}-data-bucket"
  location = var.region
}

# Subir el archivo tweets.json.zip
resource "google_storage_bucket_object" "zip_file" {
  name   = "data/tweets.json.zip"
  bucket = google_storage_bucket.data_bucket.name
  source = "${path.module}/../data/tweets.json.zip"
}

# Subir los scripts a GCS
resource "google_storage_bucket_object" "q1_memory_script" {
  name   = "src/q1_memory.py"
  bucket = google_storage_bucket.data_bucket.name
  source = "${path.module}/../src/q1_memory.py"
}

resource "google_storage_bucket_object" "q1_time_script" {
  name   = "src/q1_time.py"
  bucket = google_storage_bucket.data_bucket.name
  source = "${path.module}/../src/q1_time.py"
}

resource "google_storage_bucket_object" "q2_memory_script" {
  name   = "src/q2_memory.py"
  bucket = google_storage_bucket.data_bucket.name
  source = "${path.module}/../src/q2_memory.py"
}

resource "google_storage_bucket_object" "q2_time_script" {
  name   = "src/q2_time.py"
  bucket = google_storage_bucket.data_bucket.name
  source = "${path.module}/../src/q2_time.py"
}

resource "google_storage_bucket_object" "q3_memory_script" {
  name   = "src/q3_memory.py"
  bucket = google_storage_bucket.data_bucket.name
  source = "${path.module}/../src/q3_memory.py"
}

resource "google_storage_bucket_object" "q3_time_script" {
  name   = "src/q3_time.py"
  bucket = google_storage_bucket.data_bucket.name
  source = "${path.module}/../src/q3_time.py"
}

# Creación de la Cloud Function para ejecutar q1_memory
resource "google_cloudfunctions_function" "q1_memory_function" {
  name        = "q1_memory_function"
  description = "Function to run q1_memory"
  runtime     = "python39"
  entry_point = "execute_function"
  source_archive_bucket = google_storage_bucket.data_bucket.name
  source_archive_object = "src/q1_memory.py"
  trigger_http = true
  available_memory_mb = 256

  environment_variables = {
    DATA_PATH = "gs://${google_storage_bucket.data_bucket.name}/data/tweets.json.zip"
  }
}

# Creación de la Cloud Function para ejecutar q1_time
resource "google_cloudfunctions_function" "q1_time_function" {
  name        = "q1_time_function"
  description = "Function to run q1_time"
  runtime     = "python39"
  entry_point = "execute_function"
  source_archive_bucket = google_storage_bucket.data_bucket.name
  source_archive_object = "src/q1_time.py"
  trigger_http = true
  available_memory_mb = 256

  environment_variables = {
    DATA_PATH = "gs://${google_storage_bucket.data_bucket.name}/data/tweets.json.zip"
  }
}

# Similar configuration for other functions (q2_memory, q2_time, q3_memory, q3_time)
