class Route:
    def __init__(self, identity, sections, schedule):
        """

        :param identity: identifies the route
        :param sections: an array of the sections of the route
        :param schedule: an array of tuples representing the time (h, m). The first element is the initial
        time, so there are n + 1 times, where n is the number of sections
        """
        self.identity = identity
        self.sections = sections
        self.schedule = schedule
