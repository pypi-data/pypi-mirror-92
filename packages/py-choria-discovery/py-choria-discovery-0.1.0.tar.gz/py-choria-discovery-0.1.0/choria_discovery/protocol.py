import json

from choria_external.protocol import ProtocolMessage, Reply


@ProtocolMessage.register_protocol()
class DiscoveryRequest(ProtocolMessage):

    _protocol = 'io.choria.choria.discovery.v1.external_request'

    @staticmethod
    def create_reply():
        return DiscoveryReply()


class DiscoveryReply(Reply):

    _protocol = 'io.choria.choria.discovery.v1.external_reply'

    def __init__(self, nodes=(), error='', *args, **kwargs):
        Reply.__init__(self, *args, **kwargs)
        self.nodes = list(nodes)
        self.error = ''

    def to_json(self):
        if self.successful():
            message = json.dumps({
                'nodes': self.nodes,
            })
        else:
            message = json.dumps({
                'error': self.error,
            })
        return message

    def fail(self, error):
        self.error = error

    def successful(self):
        return self.error == ''
