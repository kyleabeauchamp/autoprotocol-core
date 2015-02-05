from autoprotocol.container import WellGroup
from autoprotocol.util import make_dottable_dict
from autoprotocol.unit import Unit

def genotyping(protocol, params):
    params = make_dottable_dict(params)
    num_samples = len(params.samples.wells)
    mastermix = protocol.ref("mastermix", None, "micro-1.5",
                             discard=True).well(0)

    protocol.transfer(params.primers.set_volume("1000:microliter"),
                      mastermix, params.primer_vol_per_rxn * Unit(num_samples, "microliter"))
    protocol.transfer(params.MyTaq_buffer.set_volume("1000:microliter"),
                      mastermix, params.buffer_vol_per_rxn * Unit(num_samples, "microliter"))
    protocol.transfer(params.MyTaq.set_volume("200:microliter"),
                      mastermix,
                      params.polymerase_vol_per_rxn*Unit(num_samples, "microliter"))
    protocol.transfer(params.water.set_volume("1000:microliter"),
                       mastermix,
                       (params.mastermix_vol_per_rxn-params.buffer_vol_per_rxn-
                       params.polymerase_vol_per_rxn-params.primer_vol_per_rxn)*Unit(num_samples, "microliter"),
                       mix_after=True,
                       mix_vol=mastermix.volume)

    protocol.distribute(mastermix,
                        params.pcr_plate.wells_from(0, num_samples),
                        params.mastermix_vol_per_rxn)

    protocol.transfer(params.samples, params.pcr_plate.wells_from(0, num_samples),
                      params.DNA_source_vol_per_rxn)

    protocol.seal(params.pcr_plate)

    protocol.thermocycle(params.pcr_plate, [
        {"cycles": 1,
         "steps": [{
            "temperature": params.activation_temp,
            "duration": params.activation_time,
            }]
         },
         {"cycles": params.pcr_cycles,
             "steps": [
                {"temperature": params.denaturation_temp,
                 "duration": params.denaturation_time},
                {"temperature": params.annealing_temp,
                 "duration": params.annealing_time},
                {"temperature": params.extension_temp,
                 "duration": params.extension_time}
                ]
        },
            {"cycles": 1,
                "steps": [
                {"temperature": "72:celsius", "duration":"2:minute"}]
            }
    ])


if __name__ == '__main__':
    from autoprotocol.harness import run
    run(genotyping, "Genotyping")
