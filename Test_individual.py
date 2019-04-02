import Simulation
from Section import Section
from Route import Route
from Bus import Bus
import Constants as ct


# ****Parameters and environment initialization****
sec1 = Section(1, 0, 0, 1200, False, ct.avg_speed)
sec2 = Section(2, 0, 5, 1500, True, ct.avg_speed)
sec3 = Section(3, 0, 10, 1450, True, ct.avg_speed)
sec4 = Section(4, 0, 0, 2400, True, ct.avg_speed)
sec5 = Section(5, 1, -10, 1450, False, ct.avg_speed)
sec6 = Section(6, 0, -5, 1500, False, ct.avg_speed)
sec7 = Section(7, 1, 0, 1200, True, ct.avg_speed)

route = Route(1, [sec1, sec2, sec3, sec4, sec5, sec6, sec7], [(8,0), (8,4), (8,8), (8,12), (8,19), (8,23), (8,27), (8,31)])

zexp = []
greenKm_expected = 0
normalKm_expected = 0
for sec in route.sections:
    zexp.append(sec.section_type)
    if sec.section_type == 1:
        greenKm_expected += sec.distance
    else:
        normalKm_expected += sec.distance

main_bus = Bus(1, route, ct.initial_charge, [3500, 2800, 1125, 800, 3000, 2200, 2340], 1.0)

[km_cov, zcov, charge] = Simulation.simulation([1, 0, 0, 0, 1, 1, 1], main_bus,zexp)
print("The expected sections to be covered\n%s" % zexp)
print("The sections covered\n%s" % zcov)
print("The remaining charge %skWh" % charge)