from base.json_to_html import converter


def main():
    converter("source.json", "index.html", tag_options=True)


if __name__ == "__main__":
    main()

