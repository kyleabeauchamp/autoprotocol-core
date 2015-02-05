import json
from autoprotocol.util import make_dottable_dict
from autoprotocol.unit import Unit

def kunkel_dilute(protocol, params):
    params = make_dottable_dict(params)

    constructs = [c for c in params.constructs if c]
    protocol.distribute(params.water,
                        params.diluted_oligo_plate.wells_from(0,len(params.constructs)),
                        params.water_vol,
                        allow_carryover=True)

    for i,c in enumerate(constructs):
        for oligo in c:
            protocol.transfer(oligo, params.diluted_oligo_plate.well(i),
                              params.oligo_vol,
                              mix_after=True,
                              mix_vol=params.water_vol/Unit(2,"microliter"))


if __name__ == '__main__':
    from autoprotocol.harness import run
    run(kunkel_dilute, "KunkelDilute")
