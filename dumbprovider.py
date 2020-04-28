from typing import Any

from pulumi import Input, Output
from pulumi.dynamic import Resource, ResourceProvider, CreateResult, CheckResult, DiffResult
import fastly
import os


class DumbProviderArgs(object):
    service_id: Input[str]
    version: Input[str]

    def __init__(self, service_id, version, dictionary_id):
        self.service_id = service_id
        self.version = version
        self.dictionary_id = dictionary_id


class DumbProviderProvider(ResourceProvider):
    def create(self, props):
        service_id = props['service_id']
        version = props['version']
        dictionary_id = props['dictionary_id']
        return CreateResult(id_=dictionary_id, outs={"dictionary_id": dictionary_id})

    def diff(self, _id: str, _olds: Any, _news: Any) -> DiffResult:
        return DiffResult(changes=False, stables=["dictionary_id", "service_id", "version"])

class DumbProviderrResource(Resource):
    service_id: Output[str]
    version: Output[str]

    def __init__(self, name, service_id, version, dictionary_id, opts=None):
        '''
        EKS auto adds 3 services, coredns, kube-proxy, and aws-node on install.
        We want to delete them so Pulumi can readd them and manage them for the life of the cluster.
        :param name:
        :param service_name:
        :param namespace:
        :param kubernetes_resource_type:
        :param kubeconfig:
        :param opts:
        '''
        args = DumbProviderArgs(service_id=service_id, version=version, dictionary_id=dictionary_id)
        full_args = {'service_id': None, 'version': None, 'dictionary_id': None, **vars(args)}
        super().__init__(DumbProviderProvider(), name, full_args, opts)
