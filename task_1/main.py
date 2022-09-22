from base.json_to_html import converter


def main():
    converter("source.json", "index.html", title="h1", body="p")


if __name__ == "__main__":
    main()
