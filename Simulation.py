from Bus import Bus
from Route import Route
from Section import Section
import Constants as ct


def simulation(zone_assignment, main_bus):
    """

    :param zone_assignment: the individual in the context of EA
    :param main_bus: all the environment configuration
    :return: the green zone which expected to covered, the green zone covered and the remaining charge
    """

    # ****Some configurations****
    zone_exp_covered = []

    for sec in main_bus.route.sections:
        zone_exp_covered.append(sec.section_type)

    zone_covered = [0 for i in range(len(main_bus.route.sections))]

    # ****Beginning of the simulation****
    if main_bus.ac:
        main_bus.charge -= main_bus.charge * ct.ac_comsuption
    for index, assignment in enumerate(zone_assignment):
        section = main_bus.route.sections[index]
        time = (section.distance * 0.001) / section.avg_speed  # hours TODO: NO ESTA SIENDO USADO AUN

        if assignment == 1: #and main_bus.charge > 0:  # if green section
            if section.slope > 0:
                main_bus.charge -= ct.light_uphill_comsuption * section.distance*0.001
            elif section.slope == 0:
                main_bus.charge -= ct.flat_comsuption * section.distance*0.001
            elif section.slope < 0:
                main_bus.charge -= ct.light_downhill_comsuption * section.distance*0.001

            if main_bus.charge >= 0:
                zone_covered[index] = 1
        #print("La bateria actual es %s" % main_bus.charge)

    return [zone_exp_covered, zone_covered, main_bus.charge]
