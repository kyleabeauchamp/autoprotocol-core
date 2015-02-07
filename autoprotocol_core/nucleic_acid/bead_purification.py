from autoprotocol.util import make_dottable_dict
from autoprotocol.unit import Unit


def bead_purification(protocol, params):
    params = make_dottable_dict(params)

    trash = protocol.ref("trash", None, "96-deep", discard=True)

    sample_plate = params.sample_plate

    samples = sample_plate.wells_from(0,
                        params.sample_number).set_volume(params.sample_volume)
    destinations = sample_plate.wells_from(
        sample_plate.well(samples.wells[-1].index + 1), params.sample_number)
    bead_volume = Unit.fromstring(params.sample_volume) * 1.8

    # Allow beads to come to room temperature

    # Resuspend the beads
    for b in params.beads:
        protocol.mix(b, volume="500:microliter")

    protocol.transfer(
        params.beads.set_volume("1500:microliter"),
        samples,
        bead_volume,
        mix_after=True,
        repetitions=20,
        mix_vol=bead_volume,
        one_source=True)


    # Let sit at RT for 10min, important, maybe longer, e.g. 20min
    protocol.incubate(
        sample_plate,
        params.initial_incubation_temp,
        params.initial_incubation_time)

    # Put into magnetic adapter for 2 minutes. Should remain here.
    protocol.plate_to_mag_adapter(
        sample_plate, params.initial_mag_adapter_time)

    for i, s in enumerate(samples.wells):
        # before adding ethanol for wash, remove all liquid from well while
        # plate is on magnet block
        protocol.transfer(
            s, trash.well(i), params.supernatant_removal_vol)

        # wash with ethanol by mixing 25x, transfer supernatant to trash
        protocol.transfer(
            params.ethanol.set_volume("1500:microliter"),
            s,
            params.ethanol_wash_vol,
            mix_after=True,
            mix_vol="50:microliter",
            repetitions=25)

        protocol.transfer(s, trash.well(i), params.wash_removal_vol)

    # Air dry for 10 minutes (often this step takes longer than 10 minutes if
    # ethanol is not removed carefully enough)
    protocol.incubate(
        params.sample_plate,
        params.ethanol_air_dry_temp,
        params.ethanol_air_dry_time)

    protocol.plate_off_mag_adapter(params.sample_plate)

    # resuspend in TE
    protocol.transfer(
        params.te.set_volume("1500:microliter"),
        samples,
        params.resuspension_vol,
        mix_after="True",
        repetitions=20,
        mix_vol=params.resuspension_vol,
        one_source=True)

    # incubate at ambient while plate is OFF the mag plate after resuspending
    # in TE
    protocol.incubate(params.sample_plate, "ambient", params.resuspension_time)

    # Put back into magnetic adapter for 5min
    protocol.plate_to_mag_adapter(
        params.sample_plate, params.final_mag_adapter_time)

    # Pipette 20ul to clean well
    protocol.transfer(samples, destinations, params.resuspension_vol)

if __name__ == '__main__':
    from autoprotocol.harness import run
    run(bead_purification, "BeadPurification")
