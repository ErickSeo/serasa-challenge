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

resource "kubernetes_cluster_role_binding" "airflow_spark_crb" {
  metadata {
    name = "airflow-spark-crb"
  }

  role_ref {
    api_group = "rbac.authorization.k8s.io"
    kind      = "ClusterRole"
    name      = "spark-operator" 
  }

  subject {
    kind      = "ServiceAccount"
    name      = "airflow-worker"
    namespace = "airflow"
  }
}


resource "kubernetes_role" "airflow_worker_role" {
  metadata {
    name      = "airflow-worker"
    namespace = "airflow"
  }

  rule {
    api_groups = [""]
    resources  = ["pods"]
    verbs      = ["*"]
  }

  rule {
    api_groups = [""]
    resources  = ["services"]
    verbs      = ["*"]
  }

  rule {
    api_groups = [""]
    resources  = ["configmaps"]
    verbs      = ["create", "get", "list", "watch", "update", "patch", "delete"]
  }

  rule {
    api_groups = [""]
    resources  = ["persistentvolumeclaims"]
    verbs      = ["create", "get", "list", "watch", "update", "patch", "delete", "deletecollection"]
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
