terraform {
  required_providers {
    kubectl = {
      source  = "gavinbunney/kubectl"
      version = ">= 1.7.0"
    }
  }
}


data "kubectl_path_documents" "scylla_cert_docs" {
    pattern = "${path.module}/manifests/cert-manager.yaml"
}

resource "kubectl_manifest" "scylla_cert" {
    count     = length(data.kubectl_path_documents.scylla_cert_docs.documents)
    yaml_body = element(data.kubectl_path_documents.scylla_cert_docs.documents, count.index)
    wait_for_rollout = true
}

data "kubectl_path_documents" "scylla_operator_docs" {
    pattern = "${path.module}/manifests/operator.yaml"
}

resource "kubectl_manifest" "scylla_operator" {
    count     = length(data.kubectl_path_documents.scylla_operator_docs.documents)
    yaml_body = element(data.kubectl_path_documents.scylla_operator_docs.documents, count.index)
    wait_for_rollout = true
}

data "kubectl_path_documents" "scylla_cluster_docs" {
    pattern = "${path.module}/manifests/cluster.yaml"
}

resource "kubectl_manifest" "scylla_cluster" {
    count     = length(data.kubectl_path_documents.scylla_cluster_docs.documents)
    yaml_body = element(data.kubectl_path_documents.scylla_cluster_docs.documents, count.index)
    wait_for_rollout = true
}