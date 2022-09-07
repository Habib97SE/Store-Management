import json
import requests
import bs4 as bs
from lxml import html
import urllib
import dotenv
import os

session_requests = requests.session()
BASE_URL = "https://fsbutiken.se"

image = ""

total_products_no = 0

error_books = 0


def create_new_product(product: dict):
    """
    Add a new product to the shopify store.
        Param : new_product : dict : The product to add which should include:
        Return : json : The product id
    """
    store_url = "https://454fbbfe5a878f728dbe109f1282fbc2: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@antbok.myshopify.com/admin"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    data = json.dumps(product)
    product_url = store_url + "/products.json"
    response = requests.post(product_url, data=data, headers=headers)
    return response.json()


def calculate_sell_price(price):
    """
    Will calculate the price of each item and send the end-user price back
        :param price: int : The ÅF price
        :return: float: The end-user price
    """
    price = float(price)
    return round(((price * 1.25) + 5) * 1.06) + 1


def find_number(text: str):
    text = text.split(" ")
    for word in text:
        if word.isdigit():
            return int(word)
    return 0


def create_inventory(text: str):
    if "100" in text:
        return 100
    if "0" in text:
        return 0
    return find_number(text)


def create_html_table(data):
    table = "<br><br><br><br>"
    table += "<div class='single_product_special_feature'><ul>"
    for key, value in data.items():
        table += "<li>" + "<strong><span class='label'>" + key + "</span>" + "<span class='desc'>" + str(
            value) + "</span>" + "</strong></li>"
    table += "</ul></div>"
    return table


def find_categories(category: str):
    # if category is empty return others
    if category == "":
        return "övriga"
    if ":" in category:
        category = category.split(":")
        category[1] = category[0] + category[1]
    return category


def login():
    HIDDEN_NAME = "ufprt"
    HIDDEN_VALUE = "E95A21779E454CF114DBF234D32C328B3A5F4217D6F87DBA99F4DF03B2CC2EAFC90D20D0E1942594D28DDF64E54D3531BD4C9A20449080BBAAC73ADB1D0D94DAB53ADFC62012431091A1EA9175A0F0501044232F59DCB3D2B5836ECEAD3B4AF08AA3846458F0B6939A0640B69D8768A4C102F3F882AB9909A1987142AC97EDD7"
    USERNAME_NAME = "loginModel.Username"
    PASSWORD_NAME = "loginModel.Password"
    LOGIN_URL = BASE_URL + "/login"
    payload = {
        USERNAME_NAME: "38446",
        PASSWORD_NAME: "habib123",
        HIDDEN_NAME: HIDDEN_VALUE,
    }
    result = session_requests.get(LOGIN_URL)
    tree = html.fromstring(result.text)
    authenticity_token = list(
        set(tree.xpath("//input[@name='" + HIDDEN_NAME + "']/@value")))[0]
    payload[HIDDEN_NAME] = authenticity_token
    result = session_requests.post(
        LOGIN_URL,
        data=payload,
        headers=dict(referer=LOGIN_URL)
    )


def edit_weight(weight):
    weight = weight.split(",")
    return weight[1]


def get_product(isbn):
    login()
    book_info = {}
    product_url = BASE_URL + "/artikel/?artikelNummer=" + isbn
    result = session_requests.get(
        product_url, headers=dict(referer=product_url))
    if result.status_code == 200:
        soup = bs.BeautifulSoup(result.text, "html.parser")
        if "Fel i visa artikel" in soup.text:
            return False
        # find img tag by class sizedimg-big
        img_tag = soup.find("img", {"class": "sizedimg-big"})
        # find the src attribute of the img tag
        img_src = img_tag.get("src")
        book_info["image"] = img_src
        div_product = soup.find("div", {"class": "artikelinfo"})
        labels = div_product.find_all("label")

        # find label with text Titel and get the text of the next label
        for label in labels:
            if label.text == "Titel":
                book_info["title"] = label.find_next_sibling("label").text
            if label.text == "Artikelnummer":
                book_info["isbn"] = label.find_next_sibling("label").text
            if label.text == "Förlag":
                book_info["publisher"] = label.find_next_sibling("label").text
            if label.text == "Språk":
                book_info["language"] = label.find_next_sibling("label").text
            if label.text == "Omfång":
                book_info["pages"] = label.find_next_sibling("label").text
            if label.text == "Utgivningsdatum":
                book_info["published_on"] = label.find_next_sibling("label").text
            if label.text == "Bandtyp":
                book_info["book_type"] = label.find_next_sibling("label").text
            if label.text == "Thema":
                book_info["categories"] = find_categories(label.find_next_sibling("label").text)
            if label.text == "Vikt":
                book_info["weight"] = edit_weight(label.find_next_sibling("label").text)
            if label.text == "F-pris":
                price = label.find_next_sibling("label").text.split(",")[0]
                book_info["price"] = calculate_sell_price(price)
            if "Författare" in label.text:
                book_info["author"] = label.text.split(",")[1].strip()
            if "Illustratör" in label.text:
                book_info["illustrator"] = label.text.split(",")[1].strip()
            if label.text == "Säljbart saldo":
                book_info["stock"] = create_inventory(label.find_next_sibling("label").text)
        # find all div with class row
        divs = soup.find_all("div", {"class": "row"})
        # find the div with class row wich has the text "Saga"
        for div in divs:
            if "Katalogtext" in div.text:
                # chekc if div has any p tags
                if div.find_all("p"):
                    # find the first p tag and get the text
                    paragraphs = div.find_all("p")
                    final_str = ""
                    for paragraph in paragraphs:
                        final_str += str(paragraph)
                    book_info["short_description"] = final_str
            if "Saga" in div.text:
                paragraphs = div.find_all("p")
                final_str = ""
                for paragraph in paragraphs:
                    final_str += str(paragraph)
                book = {
                    "Titel:": book_info["title"],
                    "ISBN:": book_info["isbn"],
                    "Förlag:": book_info["publisher"],
                    "Språk:": book_info["language"],
                    "Antal sidor:": book_info["pages"],
                    "Författare:": book_info["author"],
                    "Utgivningsdatum:": book_info["published_on"],
                    "Bokformat:": book_info["book_type"],
                }
                book_details = create_html_table(book)
                book_info["long_description"] = final_str + "<br>" + book_details
        return book_info


def write_to_file(book_info):
    with open("books.txt", "a", encoding="utf-8") as file:
        for key, value in book_info.items():
            file.write(key + ": " + str(value) + "\n")
        file.write("\n\n\n\n")


def create_product(isbn):
    book_info = get_product(str(isbn))
    if book_info is False:
        return False
    product = {
        "product": {
            "title": book_info["title"],
            "body_html": book_info["long_description"],
            "vendor": book_info["author"],
            "product_type": book_info["book_type"],
            "handle": create_handle(book_info["title"]),
            "status": "active",
            "published_at": book_info["published_on"],
            "tags": add_nyheter_tag(book_info["categories"]),
            "variants": [
                {
                    "title": book_info["book_type"],
                    "price": book_info["price"],
                    "sku": str(book_info["isbn"]),
                    "option1": book_info["book_type"],
                    "barcode": str(book_info["isbn"]),
                    "weight": book_info["weight"],
                    "weight_unit": "g",
                    "inventory_quantity": book_info["stock"],
                    "inventory_policy": "continue",
                    'fulfillment_service': "manual",
                    'inventory_management': "shopify",
                }
            ],
            "options": [
                {
                    "name": "Bokformat",
                    "values": [
                        book_info["book_type"],
                    ]
                }
            ],
            "images": [
                {
                    "alt": book_info["title"] + " av " + book_info["author"],
                    "src": book_info["image"],
                },
            ]
        }
    }

    return create_new_product(product)


def add_nyheter_tag(tags):
    if type(tags) == list:
        tags.append("nyheter")
    else:
        tags = [tags, "nyheter"]
    return tags


def find_books(url):
    page = 1
    product_exist = True
    isbns = []
    while product_exist:
        url_path = url + str(page)
        print("Retrieving data from: ", url_path)
        with urllib.request.urlopen(url_path) as response:
            html = response.read()
            soup = bs.BeautifulSoup(html, "lxml")
            div_prices = soup.find_all("div", class_="price-from")
            div_prices = list(div_prices)
            span_format = soup.find("span", class_="book-format")
            # extract src from img tag where class is product__image

            for spans in div_prices:
                unit = str(spans).split("<span>")
                if span_format.text == "E-Bok":
                    continue
                for span in unit:
                    if span.startswith("ISBN"):
                        isbn = span[5:-14]
                        isbns.append(isbn)
        if page == 600:
            return isbns
        page += 1


def create_handle(title):
    return title.replace(" ", "-").lower()


def remove_duplicates(list_of_isbns):
    return list(set(list_of_isbns))
