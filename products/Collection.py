from Communication import Communication
from Database import Database


class Collection:
    def __init__(self, title, description, image, rules):
        self.title = title
        self.description = description
        self.image = image
        self.rules = rules

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_image(self):
        return self.image

    def get_rules(self):
        return self.rules

    def set_title(self, title):
        self.title = title

    def set_description(self, description):
        self.description = description

    def set_image(self, image):
        self.image = image

    def set_rules(self, rules):
        self.rules = rules

    def to_json(self):
        return {
            "title": self.title,
            "description": self.description,
            "image": self.image,
            "rules": self.rules
        }

    def from_json(self, json):
        self.title = json["title"]
        self.description = json["description"]
        self.image = json["image"]
        self.rules = json["rules"]
        return self

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "image": self.image,
            "rules": self.rules
        }

    def from_dict(self, dict):
        self.title = dict["title"]
        self.description = dict["description"]
        self.image = dict["image"]
        self.rules = dict["rules"]
        return self

    def add_collection(self):
        data = {
            "title": self.get_title(),
            "body_html": self.get_description(),
            "image": self.get_image(),
            "rules": self.get_rules()
        }
        Communication.post("api/2022-04/smart_collections.json", data)

    def edit_collection(self, collection_id):
        data = {
            "title": self.get_title(),
            "body_html": self.get_description(),
            "image": self.get_image(),
            "rules": self.get_rules()
        }
        response = Communication.put(f"api/2022-04/smart_collections/{collection_id}.json", data)
        return response

    def __str__(self):
        return str(self.to_dict())
