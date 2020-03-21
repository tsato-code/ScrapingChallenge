#!/bin/bash

# 煮付け　カレイ　フライパン
# python crawling.py \
#     -u="https://cookpad.com/search/%E7%85%AE%E4%BB%98%E3%81%91%20%E3%82%AB%E3%83%AC%E3%82%A4%20%E3%83%95%E3%83%A9%E3%82%A4%E3%83%91%E3%83%B3?order=popularity&page=1" \
#     -o="./dataset/braised_flounder" \
#     -hu="https://cookpad.com/"

# カレー
# python crawling.py \
#     -u="https://cookpad.com//search/%E3%82%AB%E3%83%AC%E3%83%BC?order=popularity&amp;page=1" \
#      -o="./dataset/carry" \
#     -hu="https://cookpad.com/"

# 煮付け
# python crawling.py \
#     -u="https://cookpad.com/search/%E7%85%AE%E4%BB%98%E3%81%91?order=popularity&page=1" \
#     -o="./dataset/simmered" \
#     -hu="https://cookpad.com/"

# 生姜焼き
# python crawling.py \
#     -u="https://cookpad.com/search/%E7%94%9F%E5%A7%9C%E7%84%BC%E3%81%8D?order=popularity&page=1" \
#     -o="./dataset/ginger_pork" \
#     -hu="https://cookpad.com/"

# 作り置き
# python crawling.py \
#     -u="https://cookpad.com/search/%E4%BD%9C%E3%82%8A%E7%BD%AE%E3%81%8D?order=popularity&page=1" \
#     -o="./dataset/meal_prep" \
#     -hu="https://cookpad.com/"

# 肉じゃが
# python crawling.py \
#     -u="https://cookpad.com/search/%E8%82%89%E3%81%98%E3%82%83%E3%81%8C?order=popularity&page=1" \
#     -o="./dataset/meet_and_potatoes" \
#     -hu="https://cookpad.com/"

# 鍋
python crawling.py \
    -u="https://cookpad.com/search/%E9%8D%8B?order=popularity&page=1" \
    -o="./dataset/stew" \
    -hu="https://cookpad.com/"

# スイーツ
python crawling.py \
    -u="https://cookpad.com/search/%E3%82%B9%E3%82%A4%E3%83%BC%E3%83%84?order=popularity&page=1" \
    -o="./dataset/sweets" \
    -hu="https://cookpad.com/"

# おもてなし
python crawling.py \
    -u="https://cookpad.com/search/%E3%81%8A%E3%82%82%E3%81%A6%E3%81%AA%E3%81%97?order=popularity&page=1" \
    -o="./dataset/hospitality" \
    -hu="https://cookpad.com/"
