from autoprotocol.util import make_dottable_dict
from autoprotocol.unit import Unit


def golden_braid(protocol, params):
    params = make_dottable_dict(params)
    destination_plate = protocol.ref("destination_plate", None, "96-pcr",
                                      storage="cold_20")
    reaction_number = len([x for x in params.constructs if x])

    for i,construct in enumerate(params.constructs):
      if construct:
          total_frag_vol = Unit(0, "microliter")
          for fragment in construct:
              if "Concentration" in fragment.properties:
                  frag_vol = (Unit(75,"microliter")/
                              Unit(fragment.properties["Concentration"].rsplit(":")[0],
                              "microliter"))
                  total_frag_vol += frag_vol
                  protocol.transfer(fragment, destination_plate.well(i),
                                    frag_vol)
              else:
                raise RuntimeError("Fragments for Golden Braid reactions must "
                                   " have a Concentration property")

          # add mastermix
          protocol.transfer(params.mastermix, destination_plate.well(i),
                            params.mastermix_volume)
          #add water
          water_vol = Unit(10,"microliter") - (total_frag_vol + Unit(2.1,"microliter"))
          protocol.transfer(params.water, destination_plate.well(i), water_vol)

    protocol.seal("destination_plate")

    protocol.thermocycle("destination_plate", [
        {"cycles": params.golden_braid_pcr_cycles,
          "steps": [
            {"temperature": params.digestion_temp,
             "duration": params.digestion_time},
            {"temperature": params.ligation_temp,
             "duration": params.ligation_time}
        ]},
        {"cycles": 1, "steps": [
            {"temperature": "50:celsius", "duration": "10:minute"},
            {"temperature": "80:celsius", "duration": "5:minute"},
            {"temperature": "12:celsius", "duration": "10:minute"}
        ]},
    ])

if __name__ == '__main__':
    from autoprotocol.harness import run
    run(golden_braid, "GoldenBraid")
