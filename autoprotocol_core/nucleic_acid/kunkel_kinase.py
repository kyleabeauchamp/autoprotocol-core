import json
from autoprotocol.util import make_dottable_dict

def kunkel_kinase(protocol, params):
    params = make_dottable_dict(params)
    kinased_oligo_plate = protocol.ref("kinased_oligo_plate", None, "96-pcr", storage="cold_20")
    wells_to_kinase = kinased_oligo_plate.wells_from("A1", len(params.oligos))
    protocol.distribute(params.kinase_mix, wells_to_kinase,
                        params.kinase_mix_volume)

    for s,d,v in zip(params.oligos, wells_to_kinase,
                     [params.conc_oligo_volume]*len(params.oligos)):
        protocol.transfer(s, d, v, mix_after = True)

    protocol.seal(kinased_oligo_plate)

    protocol.thermocycle(kinased_oligo_plate,
    [{"cycles": 1, "steps": [
        {"temperature": params.kinase_incubation_temp,
         "duration": params.kinase_incubation_time},
        ]}
    ])

if __name__ == '__main__':
    from autoprotocol.harness import run
    run(kunkel_kinase, "KunkelKinase")
