import json
from autoprotocol.container import WellGroup
from autoprotocol.util import make_dottable_dict
from autoprotocol.unit import Unit



def kunkel(protocol, params):
    params = make_dottable_dict(params)
    kinase_oligo_plate = protocol.ref("kinase_oligo_plate", None, "96-pcr", storage="cold_20")
    wells_to_kinase = kinase_oligo_plate.wells_from("A1", len(params.oligos))
    num_oligos = 1 + len(params.oligos)
    
    #make kinase_master_mix
    kinase_mix = protocol.ref("kinase_mix", None, "micro-1.5", discard=True).well(0).set_volume("1500:microliter")
    water = protocol.ref("water", None, "micro-1.5", discard=True).well(0).set_volume("1500:microliter")

    protocol.transfer(params.PNK_buffer10x, kinase_mix, params.PNK_buffer10x_vol_per_rxn * num_oligos)
    protocol.transfer(params.ATP10mM, kinase_mix, params.ATP10mM_vol_per_rxn_kinase * num_oligos)
    protocol.transfer(params.PNK, kinase_mix, params.PNK_vol_per_rxn * num_oligos)
    protocol.transfer(water, kinase_mix, params.kinase_water_vol_per_rxn * num_oligos)

    protocol.distribute(kinase_mix, wells_to_kinase, params.kinase_MM_vol_per_rxn)



    for i, oligo in enumerate(params.oligos): protocol.transfer(oligo,
            wells_to_kinase[i], params.oligo_vol, mix_after=True,
            mix_vol=params.oligo_vol, repetitions=5)



    protocol.seal(kinase_oligo_plate)

    protocol.thermocycle(kinase_oligo_plate,
    [{"cycles": 1, "steps": [
        {"temperature": params.kinase_incubation_temp,
         "duration": params.kinase_incubation_time},
        ]}
    ])



# Step 2 - Dilute


    diluted_oligo_plate = protocol.ref("dilute_oligo_plate", None, "96-pcr", storage="cold_20")
    diluted_oligo_wells = diluted_oligo_plate.wells_from(0,len(params.combos))

    water = []
    for i in range(0,1+len(params.combos)/6):
        water.append(protocol.ref("water%s"%(i), None, "micro-1.5", discard=True ).well(0).set_volume("1000:microliter"))

    combos = [c for c in params.combos if c]
     
    protocol.distribute(water, diluted_oligo_wells, params.dilution_water_vol, allow_carryover=True)
    
    protocol.unseal(kinase_oligo_plate)

    for i,c in enumerate(combos):
        for kin_oligo in c:
            index = list(params.oligos).index(kin_oligo)
            protocol.transfer(kinase_oligo_plate.well(index), diluted_oligo_plate.well(i),
                              params.dilution_oligo_vol,
                              mix_after=True,
                              mix_vol=params.dilution_oligo_vol)


#Step 3 - Anneal

    #make ssDNA_mix from ssDNA specified
    resources_plate = protocol.ref("ssDNA_mix", None, "384-pcr", discard=True)
    ssDNA_mix = resources_plate.well(0)
    num_rxns = 2 + len(params.combos)

    protocol.transfer(params.T4_ligase_buffer10x, ssDNA_mix, params.anneal_T4_ligase_buffer10x_vol_per_rxn * num_rxns)
    protocol.transfer(params.ssDNA, ssDNA_mix, params.ssDNA_vol_per_rxn * num_rxns )




    annealing_plate = protocol.ref("annealing_oligo_plate", None, "384-pcr", storage="cold_20")
    anneal_wells = annealing_plate.wells_from(0,len(params.combos))

    protocol.distribute(ssDNA_mix, anneal_wells, params.ssDNA_mix_vol_per_rxn)

    for oligo,reaction in zip(diluted_oligo_wells.wells,anneal_wells.wells):
        protocol.transfer(oligo, reaction, params.diluted_kinased_oligo_vol, mix_after=True,
                          mix_vol=params.diluted_kinased_oligo_vol)

    protocol.seal(annealing_plate)

    protocol.thermocycle_ramp(annealing_plate,"95:celsius", "25:celsius",
                              "60:minute", step_duration="4:minute")


#Step 4 - Polymerize

    protocol.unseal(annealing_plate)

    polymerize_MM = resources_plate.well(1).set_volume("0:microliter")


    protocol.transfer(params.T4_ligase_buffer10x, polymerize_MM, params.T4_ligase_buffer10x_vol_per_rxn_polymerize * num_rxns)
    protocol.transfer(params.dNTPs_25mM, polymerize_MM, params.dNTPs_25mM_vol_per_rxn * num_rxns)
    protocol.transfer(params.ATP10mM, polymerize_MM, params.ATP10mM_vol_per_rxn_polymerize * num_rxns)
    protocol.transfer(params.T4_ligase, polymerize_MM, params.T4_ligase_vol_per_rxn * num_rxns)
    protocol.transfer(params.T7_polymerase, polymerize_MM, params.T7_polymerase_vol_per_rxn * num_rxns)


    for reaction in anneal_wells.wells:
        protocol.transfer(polymerize_MM, reaction,
                          params.polymerize_MM_vol, mix_after=True, mix_vol=params.polymerize_MM_vol)

    protocol.seal(annealing_plate)

    protocol.incubate(annealing_plate, "ambient", params.polymerize_incubation_time)


if __name__ == '__main__':
    from autoprotocol.harness import run
    run(kunkel, "Kunkel")

