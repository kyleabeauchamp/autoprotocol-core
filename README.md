#Autoprotocol-Core

This repository contains a collection of scripts that use the [autoprotocol-python](http://github.com/autoprotocol/autoprotocol-python) library to generate protocols in [Autoprotocol](https://www.autoprotocol.org), a standard way to express experiments in life science.

## Installation

    $ git clone https://github.com/autoprotocol/autoprotocol-core
    $ cd autoprotocol-core
    $ python setup.py install

##Running Protocols

All protocols in this repository require a separate config file to be passed on the command line in order to run.

For example, to run the Gibson assembly protocol:

    $ python -m autoprotocol-core.nucleic_acid.gibson_assembly path/to/gibson_config.json

Where `gibson_config.json` looks like:
```
{
  "parameters": {
    "resources": {
      "id": null,
      "type": "96-pcr",
      "storage": "cold_20"
    },
    "destination_plate": {
      "id": null,
      "type": "96-pcr",
      "storage": "cold_4",
      "discard": false
    }
    "backbone_loc": "resources/A1",
    "insert1_loc": "resources/A2",
    "insert2_loc": "resources/A3",
    "gibson_mix_loc": "resources/A4",
    "final_mix_loc": "resources/A5",
    "destination_well": "destination_plate/A1",
    "backbone_volume": "5:microliter",
    "insert1_volume": "2.5:microliter",
    "insert2_volume": "2.5:microliter",
    "gibson_mix_volume": "10:microliter",
    "gibson_reaction_time": "40:minute"
  }
}
```

Running the protocol will produce JSON-formatted autoprotocol output on
standard out.

## Contributing

The easiest way to contribute is to fork this repository and submit a pull
request.  You can also write an email to us if you want to discuss ideas or
bugs.

- Max Hodak: max@transcriptic.com
- Jeremy Apthorp: jeremy@transcriptic.com
- Tali Herzka: tali@transcriptic.com

autoprotocol-python is BSD licensed (see LICENSE). Before we can accept your
pull request, we require that you sign a CLA (Contributor License Agreement)
allowing us to distribute your work under the BSD license. Email one of the
authors listed above for more details.
