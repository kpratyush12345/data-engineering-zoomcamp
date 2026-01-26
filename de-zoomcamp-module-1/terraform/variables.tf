variable "credentials" {
  description = "Path to your Service Account json file"
  default     = "./keys/my-creds.json"
}

variable "project" {
  description = "Project ID"
  default     = "de-zoomcamp-485507"
}

variable "region" {
  description = "Region"
  default     = "us-central1"
}

variable "location" {
  description = "Project Location"
  default     = "US"
}

variable "bq_dataset_name" {
  description = "BigQuery Dataset Name"
  default     = "zoomcamp_dataset"
}

variable "gcs_bucket_name" {
  description = "GCS Bucket Name"
  default     = "de-zoomcamp-485507-data-lake-zoomcamp"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}