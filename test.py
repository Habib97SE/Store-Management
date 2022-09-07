from Communication import Communication


def main():
    isbns = []
    with open("news.txt", "r") as f:
        for line in f:
            if line == "Error\n":
                continue
            line = line.split(":")[1].strip()
            print(line)


    # for isbn in isbns:
    #     print(isbn)

if __name__ == "__main__":
    main()
