import csv
import itertools
from bs4 import BeautifulSoup
from time import sleep
import bs4
import requests
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import math

def get_urls():
    default = 'https://www.kaigoagent.com/search/prefecture_12000073?page='
    count = 1
    # 指定されたURLからHTMLを取得します
    url = f"{default}{count}"
    response = requests.get(url)
    html = response.content

    # BeautifulSoupオブジェクトを作成します
    soup = BeautifulSoup(html, "html.parser")

    total_job_counts = soup.select("div[class='bg-bg1 p-[16px]'] span[class='text-secondary max-md:text-2xl text-[32px] font-bold max-md:mx-2 ml-4']")
    print(total_job_counts[0].text.strip())
    num = int(total_job_counts[0].text.strip().replace(',', ''))
    last_nums = math.ceil(num / 20)
    sleep(3)
    urls = []
    for num in range(1, last_nums + 1):
        # 指定されたURLからHTMLを取得します
        url = f"{default}{num}"
        response = requests.get(url)
        sleep(3)
        html = response.content

        # BeautifulSoupオブジェクトを作成します
        soup = BeautifulSoup(html, "html.parser")
        # 指定されたCSSセレクタで要素を見つける
        elements = soup.select("div[class='w-full flex md:justify-evenly justify-stretch lg:p-3 md:p-1 max-md:gap-2 md:gap-4 mt-4'] a[class='colors-other2 button-rounded p-4 font-bold w-1/2 text-center !rounded-[8px] hover:opacity-70']")
        sleep(3)

        for url in elements:
            urls.append(f"https://www.kaigoagent.com{url["href"]}")
            print(urls)
    return urls
        # urlの内容を取得
# url = 'https://www.hellowork.mhlw.go.jp/kensaku/GECA110010.do?screenId=GECA110010&action=dispDetailBtn&kJNo=2707007864841&kJKbn=1&jGSHNo=V4MTZKzXtQ%2F3PbI5Eoas8Q%3D%3D&fullPart=1&iNFTeikyoRiyoDtiID=&kSNo=&newArrived=&tatZngy=1&shogaiKbn=0'

def get_job_info(url):
    html = requests.get(url).text

    # Beautifulsoup4で解析
    soup = bs4.BeautifulSoup(html, "html.parser")

    # 'table'タグ、class='normal mb1'のすべてを探します
    tables = soup.find_all('table', {'class': 'seo_table1'})

    # URLを含む辞書を初期化します
    result_dict = {'url': url}

    for table in tables:
        # その中のすべての 'tr' タグを探します。
        for tr in table.find_all('tr'):
            # 'th' タグで key を取得します。
            th = tr.find('th')
            if th:
                key = th.get_text().strip()

                # 'td' タグで value を取得します。
                td = tr.find('td')
                if td:
                    value = td.get_text().strip()

                    # 辞書に key-value ペアを追加します。
                    result_dict[key] = value

    return result_dict


# # あなたのリスト型の求人情報データ
# jobs = [{'key1': 'value1', 'key2': 'value2'}, {'key1': 'value3', 'key2': 'value4'}]

def write_to_spreadsheet(jobs):
    # 全角のキーを半角に変換し、特殊な文字を削除または置換します
    for job in jobs:
        for key in list(job.keys()):
            new_key = key.translate(str.maketrans("０１２３４５６７８９", "0123456789"))
            job[new_key] = job.pop(key).replace('\n', ' ').replace('\r', ' ')
    # pandas DataFrameに変換
    df = pd.DataFrame(jobs)

    # Google APIを使用するための認証情報（jsonファイル）
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        './service.json',
        ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']
                )

    # gspread clientの生成
    gc = gspread.authorize(credentials)

    # Google Spreadsheetを開く
    sh = gc.open_by_key('1mkeBzyj7oF0v3YEur8j1-cxLDkgI3zRshbyU077A64E')

    # ワークシートを選択（例では最初のワークシートを選択）
    worksheet = sh.worksheet("result")

    df = df.fillna("")  # NaN値を空文字（""）に置き換え

    # DataFrameをGoogle Spreadsheetに書き込む
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())

def get_sheet_a_data():
    # Google APIを使用するための認証情報（jsonファイル）
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        './service.json',
        ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    )

    # gspread clientの生成
    gc = gspread.authorize(credentials)

    # Google Spreadsheetを開く
    sh = gc.open_by_key('1mkeBzyj7oF0v3YEur8j1-cxLDkgI3zRshbyU077A64E')

    # ワークシートを選択（例ではシート名が "Sheet1" のワークシートを選択）
    worksheet = sh.worksheet("result")

    # A列のデータを全て取得
    col_values = worksheet.col_values(1)  # 1 corresponds to 'A' column

    # url格納用のlist
    urls = []

    # 確認のために取得したURLを表示
    for url in col_values:
        print(url)
        urls.append(url)

    return urls





# with open("hellowork.csv", mode="w", newline="", encoding="utf-8") as file:
#     writer = csv.writer(file)
#     # リストのデータを行ごとにCSVに書き込む
#     for row in itertools.chain.from_iterable(urls):
#         writer.writerow([row])