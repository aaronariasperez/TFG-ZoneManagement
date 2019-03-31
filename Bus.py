class Bus:
    def __init__(self, identity, route, charge, load, ac):
        """

        :param identity: identifies the bus
        :param route: the route assigned to the bus
        :param charge: the total available charge
        :param load: the total weight of the passengers for each section
        :param ac: True if the air conditioner is activated
        """
        self.identity = identity
        self.route = route
        self.charge = charge
        self.load = load
        self.ac = ac
