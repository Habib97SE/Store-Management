from Communication import Communication
from Database import Database
from Useful_Function import Function
import dotenv
import os


class Product:
    """
    The class Product is used to create a product object and manage the products.
    """
    def __init__(self, name: str, vendor: str, product_type: str, description: str, tags: list, variants: list,
                 images: list, options: list):
        """
        This class is used to create a product object.
        :param name: Title of the product
        :param vendor: The name of the vendor
        :param product_type: The type of the product
        :param description: The description of the product
        :param tags: The tags of the product
        :param variants: The variants of the product
        :param images: The images of the product
        :param options: The options of the product
        :return: A product object
        """
        self.name = name
        self.vendor = vendor
        self.product_type = product_type
        self.description = description
        self.tags = tags
        self.variants = variants
        self.images = images
        self.options = options
        self.new_communication = Communication()
        self.new_database = Database()
        self.new_function = Function()
        self.full_path = get_env_full_path()
        dotenv.load_dotenv(self.full_path + '/.env')
        self.api_version = os.getenv('API_VERSION')

    def __eq__(self, other):
        return self.get_name() == other.get_name() and self.get_vendor() == other.get_vendor() and self.get_product_type() == other.get_product_type() and self.get_description() == other.get_description() and self.get_tags() == other.get_tags() and self.get_variants() == other.get_variants() and self.get_images() == other.get_images() and self.get_options() == other.get_options()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.get_name())

    def __repr__(self):
        return {
            "name": self.get_name(),
            "vendor": self.get_vendor(),
            "product_type": self.get_product_type(),
            "description": self.get_description(),
            "tags": self.get_tags(),
            "variants": self.get_variants(),
            "images": self.get_images(),
            "options": self.get_options()
        }

    def set_name(self, name):
        self.name = name

    def set_vendor(self, vendor):
        self.vendor = vendor

    def set_product_type(self, product_type):
        self.product_type = product_type

    def set_description(self, description):
        self.description = description

    def set_tags(self, tags):
        self.tags = tags

    def set_variants(self, variants):
        self.variants = variants

    def set_images(self, images):
        self.images = images

    def set_options(self, options):
        self.options = options

    def get_options(self):
        return self.options

    def get_images(self):
        return self.images

    def get_variants(self):
        return self.variants

    def get_tags(self):
        return self.tags

    def get_name(self):
        return self.name

    def get_vendor(self):
        return self.vendor

    def get_product_type(self):
        return self.product_type

    def get_description(self):
        return self.description

    def get_product(self):
        """
        This method will create a dict with all necessary product info to post to the API.
        :return: A dict with product presentation
        """
        data = {
            "product": {
                "title": self.get_name(),
                "body_html": self.get_description(),
                "vendor": self.get_vendor(),
                "product_type": self.get_product_type(),
                "tags": self.get_tags(),
                "variants": self.get_variants(),
                "images": self.get_images(),
                "options": self.get_options()
            }
        }
        return data

    def get_product_by_id(self, product_id):
        return self.new_communication.get(f'/products/{product_id}')

    def add_product_to_website(self):
        response = self.new_communication.post('api/2022-04/products.json', self.get_product())
        if response.status_code == 201:
            self.new_database.insert_one(response.json())
        else:
            print(response.status_code)
            return False

    def find_duplicate_products(self):
        products = self.new_communication.get(self.api_version + '/products.json')
        return products.json()['products']

    def edit_product(self, product_id):
        self.new_communication.put(f'/products/{product_id}', self.get_product())

    def delete_product(self, product_id):
        self.new_communication.delete(f'/products/{product_id}')
