import json
import sys
from autoprotocol.util import make_dottable_dict
from autoprotocol.container import WellGroup

def bradford(protocol, params):
    params = make_dottable_dict(params)

    standard_plate = protocol.ref("standard_plate", None, "96-pcr", discard=True)

    standard_wells = standard_plate.wells_from(0,12 )
    wells_to_measure = params.bradford_plate.wells_from(0, ((len(standard_wells) *
        params.standard_replicates) +
        (params.sample_number * params.sample_replicates)
        + params.num_blanks), columnwise=True)
    wells_with_standard = wells_to_measure.wells[0:3*len(standard_wells)]

    blanks = wells_to_measure.wells[-1:-params.num_blanks]

    protocol.distribute(params.coomassie,
        wells_to_measure,
        "198:microliter",
        allow_carryover=True)

    protocol.serial_dilute_rowwise(params.BSA, standard_wells, "20:microliter")

    standard_start=0
    for i in range(0, params.standard_replicates):
        for s,d,v in zip(standard_wells, params.bradford_plate.wells_from(standard_start,8,columnwise=True),
                         ["2:microliter"]*8):
            protocol.transfer(s,d,v,mix_after=True, mix_vol="50:microliter")
        standard_start +=1


    sample_wells = params.bradford_plate.wells_from(standard_start,
        params.sample_number * params.sample_replicates, columnwise=True)
    start = 0
    end = 3
    for sample in params.lysates.wells:
        for i in range(start, end):
            protocol.transfer(sample, sample_wells[i], "2:microliter", mix_after=True)
        start += 3
        end += 3

    protocol.absorbance(params.bradford_plate, wells_to_measure,
        "595:nanometer", dataref="bradford")

if __name__ == '__main__':
    from autoprotocol.harness import run
    run(bradford, "BradfordAssay")
