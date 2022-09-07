import os
import requests
import json
import dotenv
from Useful_Function import Function, get_env_full_path
import Database


def response_is_ok(response):
    """
    This method is used to check if the response is ok.
    :param response: The response to check.
    :return: True if the response is ok, otherwise False.
    """
    if response.status_code == 200:
        return response.json()
    return False


def check_response(response):
    """
    This method is used to check if the response is ok.
    :param response:
    :return: if response is ok, return the response, otherwise return appropriate message.
    """
    if response["errors"]:
        return response["errors"]
    if response.status_code == 200:
        return response_is_ok(response)
    if response.status_code == 201:
        return "The request has been fulfilled and a new resource has been created."
    if response.status_code == 400:
        return """The request wasn't understood by the server, generally due to bad syntax or because 
                  the Content-Type header wasn't correctly set to application/json."""
    if response.status_code == 401:
        return "The necessary authentication credentials are not present in the request or are incorrect."
    if response.status_code == 403:
        return """The server is refusing to respond to the request. This status is generally returned 
               if you haven't requested the appropriate scope for this action."""
    if response.status_code == 404:
        return "The requested resource doesn't exist."
    # if response is not ok, then return False
    return False


def check_data_type(data):
    """
    If data is not in json, then convert it to json.
    :param data: The data to check.
    :return: The data in json format.
    """
    if type(data) is not str:
        return json.dumps(data)
    return data


def check_endpoint(self, endpoint):
    # if endpoint starts with / do nothing, else add /
    return endpoint if endpoint.startswith("/") else "/" + endpoint


class Communication:
    def __init__(self):
        useful_function = Function()
        file_path = get_env_full_path()
        dotenv.load_dotenv(file_path + "/.env")
        self.base_url = "https://%s:%s@%s.myshopify.com/admin" % (
            os.getenv("API_KEY"), os.getenv("TOKEN_ACCESS"), os.getenv("STORE_NAME"))
        self.headers = {"Accept": "application/json", "Content-Type": "application/json"}

    def get(self, endpoint: str):
        """
        This method is used to get data from the API using the GET method.
        :param endpoint: The endpoint to get data from.
        :return (dict): The data returned from the API.
        """
        endpoint = check_endpoint(self, endpoint)
        response = requests.get(self.base_url + endpoint, headers=self.headers)
        return response.json()

    def get_paginated_requests(self, url):
        """
        This method is used to get paginated requests.
        :param url: The url to get paginated requests from.
        :return: The data returned from the API.
        """
        new_db = Database.Database()
        new_db.set_collection("products")
        all_links = []
        count = 0
        while True:
            if url == "":
                break
            url = check_endpoint(self, url)
            response = requests.get(self.base_url + url, headers=self.headers)

            if len(response.json()["products"]) == 0:
                break
            for product in response.json()["products"]:
                with open("products.txt", "a") as f:
                    f.write(str(product["id"]) + "\n")
                    print(product["id"])

            if "Link" not in response.headers:
                break
            for key, value in response.headers.items():
                if key == "Link":
                    links = value.split(",")
                    for link in links:
                        if "rel=\"next\"" in link:
                            link = link.split(";")[0].replace("<", "").replace(">", "")
                            all_links.append(link)
                            url = link.split("admin")[1]
        return "Done"

    def post(self, endpoint, data):
        """
        This method is used to post data to the API using the POST method.
        :param endpoint: The endpoint to post data to.
        :param data: The data to post.
        :return: The data returned from the API.
        """
        data = json.dumps(data)
        response = requests.post(self.base_url + endpoint, data=data, headers=self.headers)
        # if response not contain error key
        return response.json()

    def put(self, endpoint, data):
        """
        This method is used to put data to the API using the PUT method.
        :param endpoint: The endpoint to put data to.
        :param data: The data to put.
        :return: The data returned from the API.
        """
        endpoint = check_endpoint(self, endpoint)
        data = json.dumps(data)
        response = requests.put(self.base_url + endpoint, headers=self.headers, data=data)
        return check_response(response)

    def delete(self, endpoint):
        """
        This method is used to delete data from the API using the DELETE method.
        :param endpoint: The endpoint to delete data from.
        :return: The data returned from the API.
        """
        endpoint = check_endpoint(self, endpoint)

        response = requests.delete(self.base_url + endpoint, headers=self.headers)
        return check_response(response)

    def get_products(self):
        """
        This method is used to get all products from the API.
        :return: The data returned from the API.
        """
        return self.get("/products")

    def find_by_title(self, title):
        """
        This method is used to find a product by name.
        :param title: The title of the product to find.
        :return: The data returned from the API.
        """
        return self.get("/products/search?query=title:" + title)

    def find_duplicate(self):
        """
        This method is used to find duplicate products.
        :return: The data returned from the API.
        """
        return self.get("/products/search?query=handle:antbok")
