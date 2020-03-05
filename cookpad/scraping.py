import csv
import datetime
import re

from bs4 import BeautifulSoup


def scraping(total_page, page_num):
    page_count = 0

    with open("dataset/recipe_data.csv", "w", newline="", encoding="utf-8") as f:
        header = ["No.", "title", "link"]
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()

    for page_num in range(total_page):
        if page_num % 10 == 0:
            print(f"{page_num}/{total_page}")
    
        with open(f"dataset/page{page_num+1}.html", "r", encoding="utf-8") as f:
            page = f.read()
        soup = BeautifulSoup(page, "lxml")

        building_list = soup.find_all("div", class_="building")
        for building in building_list:
            # カテゴリ
            building_category = building.find(class_="buildingCategory").getText()
            # 建物名
            building_name = building.find(class_="buildingName").h3.getText().replace(f"{building_category}", "")
            print(building_name)

            # CSV 書き込み
            with open("dataset/room_data.csv", "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=header)
                writer.writerow({
                    "No.": room_count, "building_name": building_name, "category": building_category
                })
            import sys
            sys.exit()



def main():
    path = "dataset/braised_flounder/data.txt"
    with open(path) as f:
        data = f.readlines()

    scraping(int(data[1].strip()), int(data[0].strip()))


if __name__ == "__main__":
    date_now = datetime.datetime.now()
    print(f"スクレイピング開始: {date_now}")
    main()
    date_now = datetime.datetime.now()
    print(f"スクレイピング終了: {date_now}")
