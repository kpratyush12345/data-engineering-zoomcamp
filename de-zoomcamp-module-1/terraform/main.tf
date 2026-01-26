terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.6.0"
    }
  }
}

provider "google" {
  credentials = file(var.credentials)
  project     = var.project
  region      = var.region
}

# Enable required APIs
resource "google_project_service" "storage_api" {
  project = var.project
  service = "storage.googleapis.com"
}

resource "google_project_service" "bigquery_api" {
  project = var.project
  service = "bigquery.googleapis.com"
}

resource "google_storage_bucket" "demo_bucket" {
  depends_on = [google_project_service.storage_api]

  name          = var.gcs_bucket_name
  location      = var.location
  storage_class = var.gcs_storage_class
  force_destroy = true

  uniform_bucket_level_access = true
}

resource "google_bigquery_dataset" "demo_dataset" {
  depends_on = [google_project_service.bigquery_api]

  dataset_id = var.bq_dataset_name
  project    = var.project
  location   = var.location
}