import json
from autoprotocol.container import WellGroup
from autoprotocol.util import make_dottable_dict
from autoprotocol.unit import Unit



def kunkel(protocol, params):
    params = make_dottable_dict(params)
    kinase_oligo_plate = protocol.ref("kinase_oligo_plate", None, "96-pcr", storage="cold_20")
    wells_to_kinase = kinase_oligo_plate.wells_from("A1", len(params.oligos))
    kinase_mix = protocol.ref("kinase_mix", None, "micro-1.5", discard=True).well(0).set_volume("1000:microliter")
    
    protocol.distribute(kinase_mix, wells_to_kinase, "23:microliter")


    for i, oligo in enumerate(params.oligos): protocol.transfer(oligo,
            wells_to_kinase[i], "7:microliter", mix_after=True,
            mix_vol="5:microliter", repetitions=5)


    protocol.seal(kinase_oligo_plate)

    protocol.thermocycle(kinase_oligo_plate,
    [{"cycles": 1, "steps": [
        {"temperature": "37:celsius",
         "duration": "60:minute"},
        ]}
    ])



# Step 2 - Dilute


    diluted_oligo_plate = protocol.ref("dilute_oligo_plate", None, "96-pcr", storage="cold_20")
    diluted_oligo_wells = diluted_oligo_plate.wells_from(0,len(params.combos))

    water = []
    for i in range(0,1+len(params.combos)/6):
        water.append(protocol.ref("water%s"%(i), None, "micro-1.5", discard=True ).well(0).set_volume("1000:microliter"))

    combos = [c for c in params.combos if c]
     
    protocol.distribute(water, diluted_oligo_wells, "198:microliter", allow_carryover=True)
    
    protocol.unseal(kinase_oligo_plate)

    for i,c in enumerate(combos):
        for kin_oligo in c:
            index = list(params.oligos).index(kin_oligo)
            protocol.transfer(kinase_oligo_plate.well(index), diluted_oligo_plate.well(i),
                              "2:microliter",
                              mix_after=True,
                              mix_vol="5:microliter")


#Step 3 - Anneal

    #ssDNA_mix from ssDNA specified, use 384-pcr to minimize dead volume
    ssDNA_mix = protocol.ref("ssDNA_mix", None, "384-pcr", discard=True).well(0).set_volume("20:microliter")

    annealing_plate = protocol.ref("annealing_oligo_plate", None, "384-pcr", storage="cold_20")

    anneal_wells = annealing_plate.wells_from(0,len(params.combos))

    protocol.distribute(ssDNA_mix, anneal_wells, "2.2:microliter")

    for oligo,reaction in zip(diluted_oligo_wells.wells,anneal_wells.wells):
        protocol.transfer(oligo, reaction, "2:microliter", mix_after=True,
                          mix_vol="2:microliter")

    protocol.seal(annealing_plate)

    protocol.thermocycle_ramp(annealing_plate,"95:celsius", "25:celsius",
                              "60:minute", step_duration="4:minute")

#Step 4 - Polymerize

    protocol.unseal(annealing_plate)

    polymerize_MM = protocol.ref("polymerize_MM", None, "384-pcr", discard=True).well(0).set_volume("20:microliter")

    for reaction in anneal_wells.wells:
        protocol.transfer(polymerize_MM, reaction,
                          "2.2:microliter", mix_after=True, mix_vol="5:microliter")

    protocol.seal(annealing_plate)

    protocol.incubate(annealing_plate, "ambient", "1.5:hour")


if __name__ == '__main__':
    from autoprotocol.harness import run
    run(kunkel, "Kunkel")

