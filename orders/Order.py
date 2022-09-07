from Communication import Communication


class Order:
    def __init__(self) -> None:
        com = Communication()

    def get_orders(self):
        end_point = "orders.json?status=any"
        return self.com.get(end_point)

    def get_order(self, id):
        end_point = "orders/%s.json" % (id)
        return self.com.get(end_point)

    def create_order(self, data: dict):
        end_point = "orders.json"
        result = self.com.post(end_point, data)
