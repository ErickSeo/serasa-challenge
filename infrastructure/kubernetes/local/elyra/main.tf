provider "kubernetes" {
  config_path = "~/.kube/config"
}

resource "kubernetes_namespace" "elyra" {
  metadata {
    name = "elyra"
  }
}

resource "kubernetes_deployment" "elyra" {
  metadata {
    name      = "elyra"
    namespace = kubernetes_namespace.elyra.metadata[0].name
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "elyra"
      }
    }

    template {
      metadata {
        labels = {
          app = "elyra"
        }
      }

      spec {
        container {
          name  = "elyra"
          image = "elyra/elyra:latest"

          port {
            container_port = 8888
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "elyra" {
  metadata {
    name      = "elyra"
    namespace = kubernetes_namespace.elyra.metadata[0].name
  }

  spec {
    selector = {
      app = "elyra"
    }

    port {
      port        = 80
      target_port = 8888
    }
  }
}
