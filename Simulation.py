import Constants as ct
import numpy as np
import random


def static_simulation(zone_assignment, main_bus):
    """

    :param zone_assignment: the individual in the context of EA
    :param main_bus: all the environment configuration
    :return: the normal and green km travelled, the zone covered and the remaining charge
    """

    zone_covered = [0 for i in range(len(main_bus.route.sections))]
    km_cov = [0] * len(main_bus.route.sections)
    charges = [0] * len(main_bus.route.sections)

    # ****Beginning of the simulation****
    for index, assignment in enumerate(zone_assignment):
        section = main_bus.route.sections[index]

        charges[index] = main_bus.charge

        # ****Charge, km covered, zones covered...****
        if assignment == 1 and main_bus.charge > 0:  # if electric chosen and there is enough charge
            dist = 0

            if section.slope >= 1:
                future_charge = main_bus.charge - (ct.light_uphill_comsuption * section.distance * 0.001) * main_bus.ac

                if future_charge >= 0:
                    dist = section.distance*0.001
                    main_bus.charge = future_charge
                    zone_covered[index] = 1
                else:
                    dist = float(main_bus.charge) / (ct.light_uphill_comsuption*main_bus.ac)
                    main_bus.charge = 0

            elif -1 < section.slope < 1:
                future_charge = main_bus.charge - (ct.flat_comsuption * section.distance * 0.001) * main_bus.ac

                if future_charge >= 0:
                    dist = section.distance * 0.001
                    main_bus.charge = future_charge
                    zone_covered[index] = 1
                else:

                    dist = float(main_bus.charge) / (ct.flat_comsuption*main_bus.ac)
                    main_bus.charge = 0

            elif section.slope <= -1:
                future_charge = main_bus.charge - (ct.light_downhill_comsuption * section.distance * 0.001) * main_bus.ac

                if future_charge >= 0:
                    dist = section.distance * 0.001
                    main_bus.charge = future_charge
                    zone_covered[index] = 1
                else:
                    dist = float(main_bus.charge) / (ct.light_downhill_comsuption*main_bus.ac)
                    main_bus.charge = 0

            km_cov[index] = dist

    charges[-1] = main_bus.charge

    return [km_cov, zone_covered, main_bus.charge, charges]


def dynamic_simulation(main_bus, model, km_normal_total, km_green_total, norm_data):
    """
    :param main_bus: all the environment configuration
    :param model: ANN of the individual
    :param norm_data: useful information for normalization [max_dist, min_dist, max_slope, min_slope]
    :return: the normal and green km travelled, the zone covered and the remaining charge
    """

    zone_covered = [0] * len(main_bus.route.sections)
    km_cov = [0] * len(main_bus.route.sections)
    charges = [0] * len(main_bus.route.sections)

    km_normal_acum = 0
    km_green_acum = 0
    zone_assignment = []
    for index, s in enumerate(main_bus.route.sections):
        norm_expected = 1 if s.section_type == 1 else -1
        norm_dist = (s.distance - norm_data[1]) / (norm_data[0] - norm_data[1])
        norm_slope = (s.slope - norm_data[3]) / (norm_data[2] - norm_data[3])
        norm_charge = main_bus.charge / ct.initial_charge
        rem_normal = km_normal_total - km_normal_acum
        norm_rem_normal = rem_normal / km_normal_total
        rem_green = km_green_total - km_green_acum
        norm_rem_green = rem_green / km_green_total
        sec = [norm_expected, norm_dist, norm_slope, norm_charge, norm_rem_normal, norm_rem_green]

        prediction = model.predict(np.array([sec]))

        if prediction[0][0] >= prediction[0][1]:  # combustion
            assignment = 0
        else:
            assignment = 1  # it has been decided to use the battery

        zone_assignment.append(assignment)

        charges[index] = main_bus.charge

        # ****Charge, km covered, zones covered...****
        if assignment == 1 and main_bus.charge > 0:  # if electric chosen and there is enough charge
            dist = 0

            if s.slope >= 1:
                r = np.random.exponential(0.5) + 1
                future_charge = main_bus.charge - (ct.light_uphill_comsuption * s.distance * 0.001) * main_bus.ac * r

                if future_charge >= 0:
                    dist = s.distance*0.001
                    main_bus.charge = future_charge
                    zone_covered[index] = 1
                else:
                    dist = float(main_bus.charge) / (ct.light_uphill_comsuption * main_bus.ac * r)
                    main_bus.charge = 0

            elif -1 < s.slope < 1:
                r = np.random.exponential(0.5) + 1
                future_charge = main_bus.charge - (ct.flat_comsuption * s.distance * 0.001) * main_bus.ac * r

                if future_charge >= 0:
                    dist = s.distance * 0.001
                    main_bus.charge = future_charge
                    zone_covered[index] = 1
                else:

                    dist = float(main_bus.charge) / (ct.flat_comsuption * main_bus.ac * r)
                    main_bus.charge = 0

            elif s.slope <= -1:
                r = np.random.exponential(0.5) + 1
                future_charge = main_bus.charge - (ct.light_downhill_comsuption * s.distance * 0.001) * main_bus.ac * r

                if future_charge >= 0:
                    dist = s.distance * 0.001
                    main_bus.charge = future_charge
                    zone_covered[index] = 1
                else:
                    dist = float(main_bus.charge) / (ct.light_downhill_comsuption * main_bus.ac * r)
                    main_bus.charge = 0

            km_cov[index] = dist

        if s.section_type == 1:
            km_green_acum += s.distance
        else:
            km_normal_acum += s.distance

    charges[-1] = main_bus.charge

    return [zone_assignment, km_cov, zone_covered, main_bus.charge, charges]
