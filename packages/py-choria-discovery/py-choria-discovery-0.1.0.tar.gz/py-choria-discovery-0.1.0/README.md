# py-choria-discovery

## Overview

`py-choria-discovery` contains a collection of tools for writing Choria External Discovery plugins in Python.

## Installation

    pip install py-choria-discovery
    
This library requires a version of Choria with external discovery support (0.19.1+).
    
## Implementing Discovery plugins

The bare minimum steps to implement a python discovery plugin are:

* Create a python file without a `.py` extension

```python
#!/usr/bin/python3
from choria_external.dispatcher import dispatch
from choria_discovery import Discovery


class MyDiscovery(Discovery):

    def discover(self):
        filtered_nodes = []
        
        # Retrieve your list of all available nodes
        #nodes = get_nodes()
        # Apply the filters in self.request.collective and self.request.filter
        #filtered_nodes = apply_filters()
        
        # Return the set of node names which match the filters
        self.reply.nodes = filtered_nodes
        

if __name__ == '__main__':
    dispatch(MyDiscovery)
```

## Example

See [examples/static](examples/static) for a basic implementation of the node filtering and response.
        
## Reference

### Discovery

Provides a base class for implementing External Discovery plugins

Public methods:

- `discover`
  Returns a boolean value to indicate whether the agent should be activated on this host.
  By default returns True and the agent is always activated. Subclasses may choose to override
  this method and deactivate themselves under appropriate conditions such as missing pre-requisites.
  
Instance variables:

- `logger`
  Contains a python logger which can be used to send log information back to choria (debug and info are sent to stdout,
  which is only displayed in verbose mode; warnings and errors are sent to stderr which are displayed always).
  The logger is set to use the `choria.plugin_name` hierarchy. By default all other logging is disabled to prevent
  pollution of the reply. This is done by setting the log level on the root logger to 100. You can re-enable
  logging by adjusting the log-level on either the root logger or a specific child if required.
- `config`
  Contains a dict-like object which can be used to read configuration settings from a choria plugin
  configuration file (`/etc/puppetlabs/mcollective/plugin.d/agentname.cfg` by default).
  
