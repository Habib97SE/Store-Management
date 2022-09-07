class Variants:
    def __init__(self, title: str, option1: str, price: str, sku: int, barcode: int, inventory_quantity: int,
                 weight: int, weight_unit: str,
                 requires_shipping: bool, position=1):
        self.title = title
        self.option1 = option1
        self.option2 = None
        self.option3 = None
        self.price = price
        self.sku = sku
        self.barcode = barcode
        self.inventory_quantity = inventory_quantity
        self.weight = weight
        self.weight_unit = weight_unit
        self.requires_shipping = requires_shipping
        self.inventor_management = "shopify"
        self.fulfillment_service = "manual"
        self.inventory_policy = "deny"
        self.compared_price = 0
        self.position = position

    def get_option1(self):
        return self.option1

    def get_option2(self):
        return self.option2

    def get_option3(self):
        return self.option3

    def get_price(self):
        return self.price

    def get_sku(self):
        return self.sku

    def get_barcode(self):
        return self.barcode

    def get_inventory_quantity(self):
        return self.inventory_quantity

    def get_weight(self):
        return self.weight

    def get_title(self):
        return self.title

    def set_compared_price(self, compared_price):
        self.compared_price = compared_price

    def set_position(self, position):
        self.position = position

    def get_position(self):
        return self.position

    def get_compared_price(self):
        return self.compared_price

    def get_inventory_management(self):
        return self.inventor_management

    def get_fulfillment_service(self):
        return self.fulfillment_service

    def set_fulfillment_service(self, fulfillment_service):
        self.fulfillment_service = fulfillment_service

    def set_inventory_management(self, inventory_management):
        self.inventor_management = inventory_management

    def set_requires_shipping(self, requires_shipping):
        self.requires_shipping = requires_shipping

    def get_inventory_policy(self):
        return self.inventory_policy

    def set_inventory_policy(self, inventory_policy):
        self.inventory_policy = inventory_policy

    def get_requires_shipping(self):
        return self.requires_shipping

    def set_title(self, title):
        self.title = title

    def get_weight_unit(self):
        return self.weight_unit

    def set_option1(self, option1):
        self.option1 = option1

    def set_option2(self, option2):
        self.option2 = option2

    def set_option3(self, option3):
        self.option3 = option3

    def set_price(self, price):
        self.price = price

    def set_sku(self, sku):
        self.sku = sku

    def set_barcode(self, barcode):
        self.barcode = barcode

    def set_inventory_quantity(self, inventory_quantity):
        self.inventory_quantity = inventory_quantity

    def set_weight(self, weight):
        self.weight = weight

    def set_weight_unit(self, weight_unit):
        self.weight_unit = weight_unit

    def __str__(self):
        return {
            "title": self.get_title(),
            "option1": self.get_option1(),
            "option2": self.get_option2(),
            "option3": self.get_option3(),
            "price": self.get_price(),
            "sku": self.get_sku(),
            "barcode": self.get_barcode(),
            "inventory_management": self.get_inventory_management(),
            "fulfillment_service": self.get_fulfillment_service(),
            "inventory_policy": self.get_inventory_policy(),
            "inventory_quantity": self.get_inventory_quantity(),
            "weight": self.get_weight(),
            "weight_unit": self.get_weight_unit(),
            "requires_shipping": self.get_requires_shipping(),
            "compare_at_price": self.get_compared_price(),
            "position": self.get_position()
        }
