from Bus import Bus
from Route import Route
from Section import Section
import Constants as ct
import numpy as np


def simulation(zone_assignment, main_bus, zexp):
    """

    :param zone_assignment: the individual in the context of EA
    :param main_bus: all the environment configuration
    :param zexp: zone which we have to cover
    :return: the normal and green km travelled, the zone covered and the remaining charge
    """

    zone_covered = [0 for i in range(len(main_bus.route.sections))]
    km_cov = [0] * len(main_bus.route.sections)
    arrival_times = [(0, 0)] * len(main_bus.route.schedule)
    arrival_times[0] = main_bus.route.schedule[0]
    charges = [0] * len(main_bus.route.sections)

    # ****Beginning of the simulation****
    for index, assignment in enumerate(zone_assignment):
        section = main_bus.route.sections[index]

        # ****Modify the arrival times****
        time = (section.distance * 0.001) / section.avg_speed  # total time
        hours = round(time)
        minutes = round(time % 1 * 60)
        if section.stop:
            normal_rand = np.random.normal(ct.stop_mean, ct.stop_deviation)
            normal_rand = 0 if normal_rand < 0 else normal_rand
            minutes += round(normal_rand)

        last_time = arrival_times[index]
        new_m = (last_time[1]+minutes) % 60
        new_h = last_time[0] + hours + (last_time[1]+minutes)//60
        new_h = new_h % 24 if new_h >= 24 else new_h

        arrival_times[index+1] = (new_h, new_m)

        charges[index] = main_bus.charge

        # ****Charge, km covered, zones covered...****
        if assignment == 1 and main_bus.charge > 0:  # if green section and there is enough charge
            dist = 0

            if section.slope > 0:
                future_charge = main_bus.charge - (ct.light_uphill_comsuption * section.distance * 0.001) * main_bus.ac

                if future_charge >= 0:
                    dist = section.distance*0.001
                    main_bus.charge = future_charge
                    zone_covered[index] = 1
                else:
                    dist = float(main_bus.charge) / (ct.light_uphill_comsuption*main_bus.ac)
                    main_bus.charge = 0

            elif section.slope == 0:
                future_charge = main_bus.charge - (ct.flat_comsuption * section.distance * 0.001) * main_bus.ac

                if future_charge >= 0:
                    dist = section.distance * 0.001
                    main_bus.charge = future_charge
                    zone_covered[index] = 1
                else:

                    dist = float(main_bus.charge) / (ct.flat_comsuption*main_bus.ac)
                    main_bus.charge = 0

            elif section.slope < 0:
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

    return [arrival_times, km_cov, zone_covered, main_bus.charge, charges]


def simulation_noSchedule(zone_assignment, main_bus, zexp):
    """

    :param zone_assignment: the individual in the context of EA
    :param main_bus: all the environment configuration
    :param zexp: zone which we have to cover
    :return: the normal and green km travelled, the zone covered and the remaining charge
    """

    zone_covered = [0 for i in range(len(main_bus.route.sections))]
    km_cov = [0] * len(main_bus.route.sections)
    charges = [0] * len(main_bus.route.sections)

    # ****Beginning of the simulation****
    for index, assignment in enumerate(zone_assignment):
        section = main_bus.route.sections[index]

        # ****Modify the arrival times****
        time = (section.distance * 0.001) / section.avg_speed  # total time
        hours = round(time)
        minutes = round(time % 1 * 60)
        if section.stop:
            normal_rand = np.random.normal(ct.stop_mean, ct.stop_deviation)
            normal_rand = 0 if normal_rand < 0 else normal_rand
            minutes += round(normal_rand)

        charges[index] = main_bus.charge

        # ****Charge, km covered, zones covered...****
        if assignment == 1 and main_bus.charge > 0:  # if green section and there is enough charge
            dist = 0

            if section.slope > 0:
                future_charge = main_bus.charge - (ct.light_uphill_comsuption * section.distance * 0.001) * main_bus.ac

                if future_charge >= 0:
                    dist = section.distance*0.001
                    main_bus.charge = future_charge
                    zone_covered[index] = 1
                else:
                    dist = float(main_bus.charge) / (ct.light_uphill_comsuption*main_bus.ac)
                    main_bus.charge = 0

            elif section.slope == 0:
                future_charge = main_bus.charge - (ct.flat_comsuption * section.distance * 0.001) * main_bus.ac

                if future_charge >= 0:
                    dist = section.distance * 0.001
                    main_bus.charge = future_charge
                    zone_covered[index] = 1
                else:

                    dist = float(main_bus.charge) / (ct.flat_comsuption*main_bus.ac)
                    main_bus.charge = 0

            elif section.slope < 0:
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
