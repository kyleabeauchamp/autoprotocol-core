from autoprotocol.container import WellGroup


def fill_384(protocol, params):
    '''
    distributes specified volume of liquid contained in "source_loc" well(s) to
    all 384 wells of the destination plate

    Parameter template:
    {
        "parameters": {
            "source_plate":{
                "id": null,
                "type": "96-deep",
                "storage": "cold_20",
                "discard": false
            },
            "destination_plate": {
                "id": null,
                "type": "384-pcr",
                "storage": "cold_20",
                "discard": false
            },
            "source_loc": [
                "source_plate/F1",
                "source_plate/F2",
                "source_plate/F3"
            ],
            "volume": "10:microliter"
        }
    }
    '''
    refs = params["refs"]

    protocol.distribute(params["source_loc"].set_volume("1500:microliter"),
        refs["destination_plate"].all_wells(), params["volume"], allow_carryover=True)


if __name__ == '__main__':
    from autoprotocol.harness import run
    run(fill_384)