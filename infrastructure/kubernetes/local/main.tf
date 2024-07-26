terraform{

}

module "k8s"{
    source = "./kind"
    cluster_name = "serasa-challenge"
    k8s_config_path = "/home/seoerick/.kube/config"
}

module "minio"{
    source = "./minio"
    k8s_config_path = "/home/seoerick/.kube/config"
}

module "kafka"{
    source = "./kafka"
    k8s_config_path = "/home/seoerick/.kube/config"
}

module "airflow"{
    source = "./airflow"
    k8s_config_path = "/home/seoerick/.kube/config"
}

module "spark"{
    source = "./spark"
    k8s_config_path = "/home/seoerick/.kube/config"
}
