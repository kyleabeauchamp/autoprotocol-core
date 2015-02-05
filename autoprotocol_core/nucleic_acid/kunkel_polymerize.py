import json
from autoprotocol.util import make_dottable_dict

def kunkel_polymerize(protocol, params):
    params = make_dottable_dict(params)

    reactions = params.reaction_plate.wells_from(0, params.number_of_rxns_to_polymerize)

    for reaction in reactions.wells:
        protocol.transfer(params.polymerize_MM, reaction,
                          params.polymerize_MM_vol, mix_after=True)

    protocol.seal("reaction_plate")

    protocol.incubate("reaction_plate", "ambient", "1.5:hour")

if __name__ == '__main__':
    from autoprotocol.harness import run
    run(kunkel_polymerize, "KunkelPolymerize")
