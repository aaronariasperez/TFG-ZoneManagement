class Section:
    def __init__(self, identity, section_type, slope, distance, stop, avg_speed):
        """

        :param identity: identifies the section
        :param section_type: 0 if normal, 1 if green
        :param slope: degrees of slope [-90,90]
        :param distance: distance of the section in meters
        :param stop: True if the section has a bus stop
        :param avg_speed: estimated average speed to travel the section
        """
        self.identity = identity
        self.section_type = section_type
        self.slope = slope
        self.distance = distance
        self.stop = stop
        self.avg_speed = avg_speed
