# variables.tf
variable "cluster_name" {
  description = "Name of the Kind cluster"
  type        = string
  default     = "data-stack"
}

variable "k8s_config_path"{
  description = "kube config path"
  type        = string
}