provider "helm" {
  kubernetes {}
}
terraform {
  required_version = ">= 1.0.0"

  required_providers {
    helm = {
      source  = "hashicorp/helm"
      version = "2.14.0"
    }
    kubectl = {
      source  = "gavinbunney/kubectl"
      version = ">= 1.7.0"
    }
  }
}

resource "kubernetes_service_account" "spark_sa" {
  metadata {
    name      = "spark"
    namespace = "processing"
  }
}

resource "kubernetes_role" "spark_role" {
  metadata {
    name      = "spark-role"
    namespace = "processing"
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

resource "kubernetes_role_binding" "spark_role_binding" {
  metadata {
    name      = "spark-role-binding"
    namespace = "processing"
  }

  role_ref {
    api_group = "rbac.authorization.k8s.io"
    kind      = "Role"
    name      = "spark-role"
  }

  subject {
    kind      = "ServiceAccount"
    name      = "spark"
    namespace = "processing"
  }
}

resource "helm_release" "spark_operator" {
  name             = "spark-operator"
  repository       = "https://kubeflow.github.io/spark-operator"
  chart            = "spark-operator"
  namespace        = "processing"
  create_namespace = true
  verify           = false
}
