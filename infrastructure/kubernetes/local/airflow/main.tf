terraform {
  required_providers {
    kubectl = {
      source  = "gavinbunney/kubectl"
      version = ">= 1.7.0"
    }
  }
}

provider "kubernetes" {
  config_path = var.k8s_config_path
}

resource "kubernetes_namespace" "airflow-ns" {
  metadata {
    name = "airflow"
  }
}


resource "kubernetes_persistent_volume" "pv_airflow_logs" {
  depends_on = [kubernetes_namespace.airflow-ns]
  metadata {
    name = "pv-airflow-logs"
  }

  spec {
    capacity = {
      storage = "2Gi"
    }
    storage_class_name = "manual"
    access_modes = ["ReadWriteMany"]

    persistent_volume_source {
      host_path {
        path = "/tmp/data"
      }
    }
  }
  }

resource "kubernetes_persistent_volume_claim" "pvc_airflow_logs" {

  depends_on = [kubernetes_persistent_volume.pv_airflow_logs]
  metadata {
    name = "pvc-airflow-logs"
    namespace = "airflow"
  }

  spec {
    access_modes = ["ReadWriteMany"]
    resources {

      requests = {
        storage = "2Gi"
      }
    }
    storage_class_name = "manual"
  }
}

resource "helm_release" "airflow" {
  depends_on = [kubernetes_namespace.airflow-ns]
  name       = "airflow"
  chart      = "apache-airflow/airflow"
  version    = "1.11.0"
  namespace  = "airflow"
  repository = " https://airflow.apache.org"
  wait       = false
  
  values = [
    "${file("${path.module}/values.yaml")}"
  ]
}
