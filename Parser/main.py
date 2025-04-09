from parser import parse_func

from db import create_db
from tw import xsl_func, save_to_db


def main():
    create_db()

    parse_func()

    data = xsl_func()

    save_to_db(data)


if __name__ == "__main__":
    main()
