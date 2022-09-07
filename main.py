import datetime
import time
from Database import Database
from Communication import Communication
from products import Product
from products import Variants
from products import Option
from products import Image
import fsbutiken
import urllib.request


def read_from_csv(file_path: str):
    """
    Read column GTIN in csv file and store all GTIN in a list.
    :param file_path: The path of the csv file.
    :return: A list of GTIN.
    """
    gtin_list = []
    isbns = []
    with open(file_path, 'r') as file:
        for line in file:
            gtin_line = line.split(",")
            for gtin in gtin_line:
                if gtin.startswith("0978"):
                    isbn = gtin.split(" ")
                    for i in isbn:
                        # remove first char in i
                        i = i[1:]
                        isbns.append(int(i))
        return isbns


def check_connection():
    try:
        response = urllib.request.urlopen("https://www.google.com")
        return True
    except:
        return False


def establish_connection():
    result = check_connection()
    if result:
        print("Connection established")
        return True
    else:
        # wait 10 sec try again
        time.sleep(10)
        print("Trying to connect again in 10 sec")
        establish_connection()


def main():
    new_com = Communication()
    new_db = Database()
    new_db.set_collection("products")

    isbns = []
    with open("lowstock.txt", "r") as f:
        for line in f:
            isbns.append(int(line))
    isbns_len = len(isbns)
    count = 0
    for isbn in isbns:
        establish_connection()
        print(str(count) + "/" + str(isbns_len) + " : " + str(isbn))
        try:
            product = fsbutiken.create_product(isbn)["product"]
            print(new_db.insert_single(product))
        except:
            print("Error")
        count += 1


if __name__ == "__main__":
    main()
