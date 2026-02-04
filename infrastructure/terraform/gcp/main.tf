terraform {
  required_version = ">= 1.5.0"
  
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# GKE Cluster
resource "google_container_cluster" "newsletter_cluster" {
  name     = "newsletter-platform-cluster"
  location = var.region
  
  initial_node_count = 3
  
  node_config {
    machine_type = "n1-standard-2"
    
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}

# Cloud SQL (PostgreSQL)
resource "google_sql_database_instance" "newsletter_db" {
  name             = "newsletter-db-instance"
  database_version = "POSTGRES_16"
  region           = var.region
  
  settings {
    tier = "db-f1-micro"
  }
}

# Cloud Pub/Sub Topics
resource "google_pubsub_topic" "newsletter_events" {
  name = "newsletter-events"
}

# Cloud Storage Bucket
resource "google_storage_bucket" "newsletter_storage" {
  name     = "${var.project_id}-newsletter-storage"
  location = var.region
}
