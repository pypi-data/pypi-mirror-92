import logging

from choria_external.base import ChoriaExternal

# Ensure the protocol messages are loaded and registered
import choria_discovery.protocol


class Discovery(ChoriaExternal):
    """ Base class for External Discovery requests
    """

    def discover(self):
        """ Implement the node discovery action
            This method should be overridden by subclasses
        """
        pass

    def execute(self):
        self.discover()
