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

data "kubectl_path_documents" "docs" {
    pattern = "${path.module}/manifest.yaml"
}

resource "kubectl_manifest" "spark_manifest" {
    count     = length(data.kubectl_path_documents.docs.documents)
    yaml_body = element(data.kubectl_path_documents.docs.documents, count.index)
}


resource "helm_release" "spark_operator" {
  name             = "spark-operator"
  repository       = "https://kubeflow.github.io/spark-operator"
  chart            = "spark-operator"
  namespace        = "processing"
  create_namespace = true
  verify           = false
}
