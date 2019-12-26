import click
from kubernetes import client, config

config.load_kube_config()
v1 = client.CoreV1Api()

def get_namespace(namespace):
    ns = v1.list_namespace(field_selector=f'metadata.name={namespace}')
    if not ns.items:
        raise ValueError(f"namespace {namespace} not found")
    return ns.items[0]

@click.command()
@click.argument("namespace")
def delete(namespace):
    ns = get_namespace(namespace)
    if ns.status.phase != 'Terminating':
        raise ValueError("not in terminating phase")
    ns.spec.finalizers = []
    resp = v1.replace_namespace_finalize(namespace, ns)

if __name__ == '__main__':
    delete()
