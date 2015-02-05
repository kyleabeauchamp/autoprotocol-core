import math
from autoprotocol.util import make_dottable_dict


def growth_curve(protocol, params):
    params = make_dottable_dict(params)

    growth_plate = protocol.ref(
        "growth_plate",
        cont_type="96-flat",
        storage="cold_4")
    num_curves = (
        len(params.samples) * params.replicates
        + params.num_negative_controls
    )
    num_columns = int(math.ceil(
        num_curves / float(growth_plate.container_type.row_count())))
    protocol.dispense(growth_plate, "lb-broth-noAB", [
        {'column': i, 'volume': '80:microliter'}
        for i in xrange(num_columns)
        ])
    sample_wells = growth_plate.wells_from("A1", num_curves, columnwise=True)

    samples = sum([[s] * params.replicates for s in params.samples], [])

    for aliquot, dest in zip(samples, sample_wells):
        protocol.transfer(aliquot, dest, params.sample_vol, mix_after=True)

    incubate_time = params.total_growth_time / params.num_reads
    protocol.cover(growth_plate)
    for i in xrange(params.num_reads):
        protocol.incubate(
            growth_plate,
            where="warm_37",
            shaking=True,
            duration=incubate_time)
        protocol.absorbance(
            growth_plate,
            sample_wells,
            "600:nanometer",
            dataref=("OD600_%d" % (i+1)))

if __name__ == '__main__':
    from autoprotocol.harness import run
    run(growth_curve, 'GrowthCurve')
