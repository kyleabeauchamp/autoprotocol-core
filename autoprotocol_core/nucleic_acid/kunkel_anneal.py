import json
from autoprotocol.util import make_dottable_dict

def kunkel_anneal(protocol, params):
    params = make_dottable_dict(params)

    anneal_wells = params.annealing_plate.wells_from(0,len(params.diluted_oligos))

    protocol.distribute(params.ssDNA_mix,anneal_wells, params.ssDNA_mix_vol)

    for oligo,reaction in zip(params.diluted_oligos,anneal_wells.wells):
        protocol.transfer(oligo, reaction, params.oligo_vol, mix_after=True,
                          mix_vol="2:microliter")

    protocol.seal(params.annealing_plate)

    protocol.thermocycle_ramp("annealing_plate","95:celsius", "25:celsius",
                              "60:minute", step_duration="4:minute")

if __name__ == '__main__':
    from autoprotocol.harness import run
    run(kunkel_anneal, "KunkelAnneal")
