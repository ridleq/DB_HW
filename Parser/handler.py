import xlrd
import os
from datetime import datetime


from db import Session, TradeRes

directory = "downloaded_files"

data = []
found_table = False
headers = {}


def is_numeric(value):
    try:
        float(value.replace(',', '.'))
        return True
    except ValueError:
        return False


def xsl_func():
    global found_table
    global headers
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        workbook = xlrd.open_workbook(filepath)
        sheet = workbook.sheet_by_index(0)

        date_info = sheet.cell_value(3, 1)
        if "Дата торгов:" in date_info:
            trade_date_on = date_info.split("Дата торгов:")[-1].strip()
            trade_date_object = datetime.strptime(trade_date_on, "%d.%m.%Y")
            formatted_trade_date = trade_date_object.strftime("%Y-%m-%d")

        for row_idx in range(sheet.nrows):
            row = sheet.row_values(row_idx)
            if "".join(row).strip() == "Единица измерения: Метрическая тонна":
                found_table = True
            elif found_table:
                if any(row):
                    if not headers:
                        headers = {
                            header.lower().replace("\n", " "): idx
                            for idx, header in enumerate(row)
                        }
                    else:
                        exchange_product_id = row[headers["код инструмента"]]
                        exchange_product_name = row[
                            headers["наименование инструмента"]
                        ]
                        delivery_basis_name = row[headers["базис поставки"]]
                        volume_value = row[
                            headers["объем договоров в единицах измерения"]
                        ]

                        volume = (
                            float(volume_value) if is_numeric(
                                volume_value
                            ) else 0.0
                        )
                        total_value = row[headers["обьем договоров, руб."]]
                        total = (
                            float(total_value) if is_numeric(
                                total_value
                            ) else 0.0
                        )
                        count_value = row[headers["количество договоров, шт."]]
                        count = (
                            int(count_value) if count_value.isdigit() else 0
                        )

                        if count > 0 and exchange_product_id not in (
                            "Итого:",
                            "Итого по секции:",
                        ):
                            data.append(
                                {
                                    "exchange_product_id": exchange_product_id,
                                    "exchange_product_name": exchange_product_name,
                                    "delivery_basis_name": delivery_basis_name,
                                    "volume": volume,
                                    "total": total,
                                    "count": count,
                                    "date": formatted_trade_date
                                }
                            )
    return data


def save_to_db(data):
    session = Session()
    for item in data:
        exchange_product_id = item["exchange_product_id"]
        oil_id = exchange_product_id[:4]
        delivery_basis_id = exchange_product_id[4:7]
        delivery_type_id = exchange_product_id[-1]

        trade_res = TradeRes(
            exchange_product_id=exchange_product_id,
            exchange_product_name=item["exchange_product_name"],
            oil_id=oil_id,
            delivery_basis_id=delivery_basis_id,
            delivery_basis_name=item["delivery_basis_name"],
            delivery_type_id=delivery_type_id,
            volume=item["volume"],
            total=item["total"],
            count=item["count"],
            date=item["date"],
            created_on=datetime.now(),
            updated_on=datetime.now()
        )
        session.add(trade_res)
    session.commit()
    session.close()


if __name__ == "__main__":
    data = xsl_func()
    save_to_db(data)
