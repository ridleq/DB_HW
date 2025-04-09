import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os


def parse_func():
    link = "https://spimex.com/markets/oil_products/trades/results/?page=page-"
    link_for_download = "https://spimex.com"
    add_for_link = 1
    valid_date = datetime(2023, 1, 1)

    download_directory = "downloaded_files"
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)

    file_counter = 1

    while True:
        response = requests.get(f"{link}{add_for_link}").text
        soup = BeautifulSoup(response, 'lxml')
        block = soup.find('div', class_='page-content__tabs')
        all_files = block.find_all('div', class_='accordeon-inner__wrap-item')

        files_found = False

        for file in all_files:
            file_link = file.find('a').get('href')
            if 'oil_xls' in file_link:
                date_text = file.find('span').text.strip()
                file_date = datetime.strptime(date_text, '%d.%m.%Y')
                if file_date > valid_date:
                    files_found = True
                    download_response = requests.get(
                        f"{link_for_download}{file_link}"
                    )
                    file_name = os.path.join(
                        download_directory, f"{file_counter}.xls"
                    )
                    with open(file_name, 'wb') as f:
                        f.write(download_response.content)
                    file_counter += 1

        if not files_found:
            break

        add_for_link += 1


if __name__ == "__main__":
    parse_func()
