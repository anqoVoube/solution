from base.json_to_html import converter


def main():
    converter("source.json", "index.html", table_like=True)


if __name__ == "__main__":
    main()

