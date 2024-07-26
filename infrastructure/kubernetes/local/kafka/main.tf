terraform {
  required_providers {
    kubectl = {
      source  = "gavinbunney/kubectl"
      version = ">= 1.7.0"
    }
  }
}

data "kubectl_path_documents" "docs" {
    pattern = "${path.module}/manifest.yaml"
}

resource "kubectl_manifest" "kafka" {
    count     = length(data.kubectl_path_documents.docs.documents)
    yaml_body = element(data.kubectl_path_documents.docs.documents, count.index)
}