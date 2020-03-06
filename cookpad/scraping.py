import csv
import datetime
import re
import urllib.parse

from bs4 import BeautifulSoup


HOME_URL = "https://cookpad.com"
OUT_DIR = "dataset/braised_flounder"


def scraping(total_page, _num):
    recipe_no = 0

    with open(f"{OUT_DIR}/data_links.csv", "w", newline="", encoding="utf-8") as f:
        header = ["No.", "title", "author", "abstract", "material", "link"]
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()

    for page_num in range(total_page):
        if page_num % 10 == 0:
            print(f"{page_num}/{total_page}")
    
        with open(f"{OUT_DIR}/page{page_num+1:000006}.html", "r", encoding="utf-8") as f:
            page = f.read()
        soup = BeautifulSoup(page, "lxml")

        recipe_list = soup.find_all("div", class_="recipe-text")
        for recipe in recipe_list:
            # タイトル
            recipe_title = recipe.find("h2", class_="title font16").text.strip()
            # 著者
            recipe_author = recipe.find("span", class_="font12 recipe_author_name").text.strip("by\n")
            # 概要
            recipe_abstract = recipe.find("div", class_="recipe_description").text.strip("\n...").replace("\n", "")
            # 材料
            recipe_material = recipe.find("div", class_="material ingredients").text.strip("\n...").replace("\n", "")
            # レシピリンク
            recipe_link = recipe.find("a", class_="recipe-title font13").attrs["href"]
            recipe_link = urllib.parse.urljoin(HOME_URL, recipe_link)

            # CSV 書き込み
            with open(f"{OUT_DIR}/data_links.csv", "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=header)
                writer.writerow({
                    "No.": recipe_no,
                    "title": recipe_title,
                    "author": recipe_author,
                    "abstract": recipe_abstract,
                    "material": recipe_material,
                    "link": recipe_link
                })
            recipe_no += 1


def main():
    path = f"{OUT_DIR}/data.txt"
    with open(path) as f:
        data = f.readlines()

    scraping(int(data[1].strip()), int(data[0].strip()))


if __name__ == "__main__":
    date_now = datetime.datetime.now()
    print(f"スクレイピング開始: {date_now}")
    main()
    date_now = datetime.datetime.now()
    print(f"スクレイピング終了: {date_now}")
