from bs4 import BeautifulSoup
import datetime
import csv
import re

# 住所を都道府県と市区町村に分ける用の正規表現
pat = '(...??[都道府県])((?:旭川|伊達|石狩|盛岡|奥州|田村|南相馬|那須塩原|東村山|武蔵村山|羽村|十日町|上越|富山|野々市|大町|蒲郡|四日市|姫路|大和郡山|廿日市|下>松|岩国|田川|大村|宮古|富良野|別府|佐伯|黒部|小諸|塩尻|玉野|周南)市|(?:余市|高市|[^市]{2,3}?)郡(?:玉村|大町|.{1,5}?)[町村]|(?:.{1,4}市)?[^町]{1,4}?区|.{1,7}?[市町村])(.+)'

def scraping(total_page, room_num):
    # 物件数の初期化
    room_count = 0

    # csvファイルの準備（ヘッダーをつける）
    with open('room_data.csv', 'w', newline='', encoding='utf-8') as file:
        header = ['No', 'building_name', 'category', 'prefecture', 'city', 'station_num', 'station', 'method', 'time', 'age', 'total_stairs', 'stairs', 'layout', 'room_num', 'space', 'south', 'corner', 'rent', 'unit_price', 'url']
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()


    for page_num in range(total_page):
        # スクレイピングの進捗出力
        if page_num % 10 == 0:
            print(page_num , '/', total_page)

        # スクレイピングするhtmlファイルをBeautifulSoupで開く
        with open('./html_files/page{}.html'.format(page_num + 1), 'r', encoding='utf-8') as file:
            page = file.read()
        soup = BeautifulSoup(page, "lxml")

        # 建物ごとに情報を取得
        building_list = soup.find_all("div", class_="building")
        for building in building_list:
            # 建物カテゴリー：マンション or アパート or 一戸建て
            buildingCategory = building.find(class_="buildingCategory").getText()

            # 建物名
            buildingName = building.find(class_="buildingName").h3.getText().replace("{}".format(buildingCategory), "").replace("新着あり", "")

            # 最寄駅と駅からの距離の候補抽出
            traffic = building.find("ul", class_="traffic").find_all("li")
            # 最寄駅の数
            station_num = len(traffic)
            # 徒歩時間が短いものを抽出する
            min_time = 1000000    # 所要時間の最小値初期化
            for j in range(station_num):
                traffic[j] = traffic[j].text
                figures = re.findall(r'\d+', traffic[j])
                time = 0
                for figure in figures:
                    # 所要時間の計算
                    time += int(figure)
                # 最小だったら最小所要時間とインデックスを保管
                if time < min_time:
                    min_time = time
                    index = j

            # 駅や路線の情報がある場合
            if len(traffic[index].split(' ')) > 1:
                # 路線の決定
                line = traffic[index].split(' ')[0]
                # 最寄り駅の決定
                station = traffic[index].split(' ')[1].split('駅')[0]
                # 駅までの交通手段（バス・車・徒歩）の取得
                if len(traffic[index].split(' ')) > 2:
                    if "バス" in traffic[index].split(' ')[1]:
                        method = "bus"
                    elif "車" in traffic[index].split(' ')[2]:
                        method = "car"
                    else:
                        method = "walk"
                # 駅までの交通手段情報なし
                else:
                    method = None
            # 駅や路線の情報がない場合
            else:
                station = None
                line = None
                method = None
                time = None

            # 住所
            address = building.find(class_="address").getText().replace('\n','')
            address = re.split(pat, address)
            if len(address) < 3:
                prefecture = "東京都"
                city = "足立区"
            else:
                prefecture = address[1]
                city = address[2]

            # 建物の詳細（築年数・構造・総階数）
            building_detail = building.find(class_="detailData").find_all("td")
            for j in range(len(building_detail)):
                building_detail[j] = building_detail[j].text

            # ----築年数の数値だけ取得----
            # 築年数不詳
            if '築不詳' == building_detail[0]:
                building_detail[0] = None
            # 築0年
            elif '未満' in building_detail[0]:
                building_detail[0] = 0
            # 正常な値
            else:
                building_detail[0] = int(re.findall(r'\d+', building_detail[0])[0])

            # 総階数の数値だけ取得
            building_detail[2] = int(re.findall(r'\d+', building_detail[2])[0])


            # ---- 部屋の詳細取得 ----
            rooms = building.find(class_="detail").find_all("tr",
                                                            {'class': ['estate applicable', 'estate applicable gray']})
            for j in range(len(rooms)):
                # 物件数のカウント
                room_count += 1

                # ---- 階数 ----
                stairs = rooms[j].find("td", class_="roomNumber").text
                # 数値だけ取得（「階」削除、欠損値処理）
                if "-" == stairs:
                    stairs = None
                else:
                    stairs = int(re.findall(r'\d+', stairs)[0])

                # 家賃を整数型にする
                price = rooms[j].find(class_="roomPrice").find_all("p")[0].text
                price = round(10000 * float(price.split('万')[0]))

                # 管理費
                kanri_price = rooms[j].find(class_="roomPrice").find_all("p")[1].text
                # 表記の統一（万円表記の削除、「-」と「0円」の欠損値処理）
                if "-" in kanri_price or "0円" == kanri_price:
                    kanri_price = 0
                else:
                    kanri_price = int(kanri_price.split('円')[0].replace(',',''))

                # 部屋タイプ（間取り）
                room_type = rooms[j].find(class_="type").find_all("p")[0].text
                if room_type == "ワンルーム":
                    room_type = "1R"
                # 部屋数
                num_of_rooms = int(re.findall(r'\d+', room_type)[0])


                # 部屋の面積、単位「m2」の削除
                room_area = rooms[j].find(class_="type").find_all("p")[1].text
                room_area = float(room_area.split('m')[0])

                # 南向き・角部屋
                special = rooms[j].find_all("span", class_="specialLabel")
                south = 0
                corner = 0
                for label in range(len(special)):
                    if "南向き" in special[label].text:
                        south = 1
                    if "角部屋" in special[label].text:
                        corner = 1

                # 詳細urlを取得
                room_url = rooms[j].find("td", class_="btn").a.get('href')

                # 家賃 = 賃料+管理費　を求める
                rent = price + kanri_price

                # 1m^2ごとの家賃（単価）を求める
                unit_price = rent / room_area

                # csvファイルへの出力：encordingデフォルトは"utf-8""
                with open('room_data.csv', 'a', newline='', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames=header)
                    writer.writerow(
                        {'No':room_count, 'building_name':buildingName, 'category':buildingCategory, 'prefecture':prefecture, 'city':city, 'station_num':station_num, 'station':station,
                              'method':method, 'time':min_time, 'age':building_detail[0], 'total_stairs':building_detail[2], 'stairs':stairs,
                              'layout':room_type, 'room_num':num_of_rooms, 'space':room_area, 'south':south, 'corner':corner, 'rent':rent, 'unit_price':unit_price, 'url':room_url})

    print("{}件の物件データを取得しました。".format(room_count))
    #検収条件の確認
    if room_count == room_num:
        print("検収条件をクリア")
    else:
        print("{}件の差異があります。検収条件をクリアしていません。".format(abs(room_count-room_num)))

if __name__ == "__main__":
    date_now = datetime.datetime.now()
    print("スクレイピング開始：", date_now)
    # 総ページ数と物件数をスクレイピング関数に渡す（検収条件）
    path = './data.txt'
    with open(path) as f:
        data = f.readlines()
    scraping(int(data[1].replace("\n","")), int(data[0].replace("\n","")))
    date_now = datetime.datetime.now()
    print("スクレイピング終了：", date_now)