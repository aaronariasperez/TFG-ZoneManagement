class Bus:
    def __init__(self, identity, route, charge, ac):
        """

        :param identity: identifies the bus
        :param route: the route assigned to the bus
        :param charge: the total available charge
        :param load: the total weight of the passengers for each section
        :param ac: extra consumption of the ac
        """
        self.identity = identity
        self.route = route
        self.charge = charge
        self.ac = ac
