import os


def get_env_full_path():
    file_path = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Antbok")
    return file_path


class Function:
    """
    | This class includes all the functions that are used in the project.
    | List of all functions:
    | 1- find_id_by_custom_filter: This function is used to find a specific value in a dict.
    | 2- get_env_full_path: This function is used to get the full path of the .env file.
    """

    def find_id_by_custom_filter(self, data: dict, name: str):
        for key, value in data.items():
            if key == name:
                return value
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        self.find_id_by_custom_filter(item)
        return None

    def get_all_products(self, new_com, new_db):
        """
        This function is used to get all products from the API.
        :param new_com: The Communication object.
        :param new_db: The Database object.
        :return: A list of all products.
        """
        count = 0
        while True:
            products = new_com.get("products.json?since_id=" + str(count))['products']
            if len(products) == 0:
                print("No products found")
                break
            print(str(len(products)) + " products have been found.")
            for product in products:
                new_db.set_collection("products")

                print("Insert new product to database " + str(product['id']) + ": ", end=" ")
                print(new_db.insert_single(product))
            count += 1
            products.clear()
