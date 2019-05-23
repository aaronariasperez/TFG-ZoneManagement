class Section:
    def __init__(self, identity, section_type, slope, distance):
        """

        :param identity: identifies the section
        :param section_type: 0 if normal, 1 if green
        :param slope: degrees of slope [-90,90]
        :param distance: distance of the section in meters
        """
        self.identity = identity
        self.section_type = section_type
        self.slope = slope
        self.distance = distance
