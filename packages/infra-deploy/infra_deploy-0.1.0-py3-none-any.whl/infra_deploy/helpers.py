from kubernetes import client as kli
from kubernetes.client import V1Deployment

DEPLOYMENT_NAME = "core-rust-server"


def create_test_container():
    # Configureate Pod template container
    container = kli.V1Container(
        name="core-api-service",
        image="aimvector/python:1.0.4",
        image_pull_policy="Always",
        ports=[kli.V1ContainerPort(container_port=5000)],
        resources=kli.V1ResourceRequirements(
            requests=dict(cpu="50m",
                          memory="64Mi"),
            limits=dict(cpu="50m",
                        memory="64Mi"),
        )
    )
    # client.V1DeploymentStrategy()
    # Create the specification of deployment
    return container


def built_test_pod():
    container = create_test_container()
    return kli.V1PodSpec(containers=[container])


def built_test_pod_template():
    pod = built_test_pod()
    template = kli.V1PodTemplateSpec(
        metadata=kli.V1ObjectMeta(labels={"app": "nginx"}),
        spec=pod
    )
    return template


def built_test_deploy_spec():
    template = built_test_pod_template()
    deploy_spec = kli.V1DeploymentSpec(
        replicas=3,
        template=template,
        selector={'matchLabels': {
            'app': 'nginx'
        }}
    )
    return deploy_spec


def built_test_deploy() -> V1Deployment:
    deploy_spec = built_test_deploy_spec()
    deployment = kli.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=kli.V1ObjectMeta(name=DEPLOYMENT_NAME),
        spec=deploy_spec
    )
    return deployment
