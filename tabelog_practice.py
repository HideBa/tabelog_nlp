import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time

class Tabelog:
    """
    食べログスクレイピングクラス
    test_mode=Trueで動作させると、最初のページの３店舗のデータのみを取得できる
    pretest=Trueで動作させるとプレ解析
    """
    def __init__(self, base_url, test_mode=True, pretest=False, p_ward='東京都内', begin_page=1, end_page=30):

        # 変数宣言
        self.store_id = ''
        self.store_id_num = 0
        self.store_name = ''
        self.store_score = 0
        self.pretest = pretest
        self.ward = p_ward
        self.lunch_price = ''
        self.dinner_price = ''
        self.lunch = False
        self.dinner = False

        self.cuisine = '-'
        self.service = '-'
        self.atmos = '-'
        self.cp = '-'
        self.drink = '-'

        self.review_cnt = 0
        self.score = 0
        self.lunch_review = ''
        self.dinner_review = ''
        #self.review = ''
        self.columns = ['store_id', 'store_name', 'store_score', 'ward', 'lunch', 'dinner', '料理・味', 'サービス', '雰囲気', 'CP', '酒・ドリンク', 'review_cnt', 'score','lunch_review', 'dinner_review']
        self.df = pd.DataFrame(columns=self.columns)
        self.__regexcomp = re.compile(r'\n|\s') # \nは改行、\sは空白

        page_num = begin_page # 店舗一覧ページ番号

        if test_mode:
            list_url = base_url + str(page_num) +  '/?Srt=D&SrtT=rt&sort_mode=1' #食べログの点数ランキングでソートする際に必要な処理
            self.scrape_list(list_url, mode=test_mode)
        else:
            while True:
                list_url = base_url + str(page_num) +  '/?Srt=D&SrtT=rt&sort_mode=1' #食べログの点数ランキングでソートする際に必要な処理
                if self.scrape_list(list_url, mode=test_mode) != True:
                    break

                # INパラメータまでのページ数データを取得する
                if page_num >= end_page:
                    break
                page_num += 1
        return

    def scrape_list(self, list_url, mode):
        """
        店舗一覧ページのパーシング
        お店がたくさん並んでいるページをスクレイピング
        """
        # try:
        #     html = urllib.request.urlopen(_Url)
        # except urllib.error.HTTPError as e:
        #     print(e.code)
        #     sleep(60)
        #     html = urllib.request.urlopen(_Url)

        r = requests.get(list_url)
        time.sleep(5)
        if r.status_code != requests.codes.ok:
            return False

        soup = BeautifulSoup(r.content, 'html.parser')
        soup_a_list = soup.find_all('a', class_='list-rst__rst-name-target') # 店名一覧
        

        if len(soup_a_list) == 0:
            return False
        
        # プレ解析なら指定されたurlをパーシング
        # 上から順にきよ田、三谷、いまむら、初音鮨、さわだ、青空、すし通、まつ勘、銀座　鮨一

        if self.pretest:
            url_list = ["https://tabelog.com/tokyo/A1301/A130101/13070238/",
                        "https://tabelog.com/tokyo/A1309/A130902/13042204/",
                        "https://tabelog.com/tokyo/A1316/A131602/13096905/",
                        "https://tabelog.com/tokyo/A1315/A131503/13017742/",
                        "https://tabelog.com/tokyo/A1301/A130101/13001043/",
                        "https://tabelog.com/tokyo/A1301/A130103/13032283/",
                        "https://tabelog.com/tokyo/A1307/A130701/13061640/",
                        "https://tabelog.com/tokyo/A1307/A130702/13001680/",
                        "https://tabelog.com/tokyo/A1301/A130101/13024567/",
                        ]
            if mode:
                for url in url_list[7:]:
                    item_url = url # 店の個別ページURLを取得
                    self.store_id_num += 1
                    self.scrape_item(item_url, mode)
            else:
                for url in url_list:
                    item_url = url # 店の個別ページURLを取得
                    self.store_id_num += 1
                    self.scrape_item(item_url, mode)

        else:
            if mode:
                for soup_a in soup_a_list[:1]:
                    print(soup_a)
                    item_url = soup_a.get('href') # 店の個別ページURLを取得
                    self.store_id_num += 1
                    self.scrape_item(item_url, mode)
            else:
                for soup_a in soup_a_list:
                    item_url = soup_a.get('href') # 店の個別ページURLを取得
                    self.store_id_num += 1
                    self.scrape_item(item_url, mode)



        return True

    def scrape_item(self, item_url, mode):
        """
        個別店舗情報ページのパーシング
        """
        start = time.time()

        r = requests.get(item_url)
        time.sleep(5)
        if r.status_code != requests.codes.ok:
            print(f'error:not found{ item_url }')
            return

        soup = BeautifulSoup(r.content, 'html.parser')
        #print(r.content)
        #print(soup.find('li', {'spam': re.compile('20,000')}))
        # 店舗名称取得
        # <h2 class="display-name">
        #     <span>
        #         麺匠　竹虎 新宿店
        #     </span>
        # </h2>
        store_name_tag = soup.find('h2', class_='display-name')
        store_name = store_name_tag.span.string
        print('{}→店名：{}'.format(self.store_id_num, store_name.strip()), end='')
        self.store_name = store_name.strip()

        # ラーメン屋、つけ麺屋以外の店舗は除外
        store_head = soup.find('div', class_='rdheader-subinfo') # 店舗情報のヘッダー枠データ取得
        store_head_list = store_head.find_all('dl')
        store_head_list = store_head_list[1].find_all('span')
        #print('ターゲット：', store_head_list[0].text)

        if store_head_list[0].text not in {'寿司'}:
            print('お寿司屋さんではないので処理対象外')
            self.store_id_num -= 1
            return

        # 評価点数取得
        #<b class="c-rating__val rdheader-rating__score-val" rel="v:rating">
        #    <span class="rdheader-rating__score-val-dtl">3.58</span>
        #</b>
        rating_score_tag = soup.find('b', class_='c-rating__val')
        rating_score = rating_score_tag.span.string
        print('  評価点数：{}点'.format(rating_score), end='')
        self.store_score = rating_score

        # 評価点数が存在しない店舗は除外
        if rating_score == '-':
            print('  評価がないため処理対象外')
            self.store_id_num -= 1
            return
       # 評価が3.5未満店舗は除外
        # if float(rating_score) < 3.5:
        #     print('  食べログ評価が3.5未満のため処理対象外')
        #     self.store_id_num -= 1
        #     return

        # 昼と夜それぞれの時間帯の価格を取得
        landd_tag = soup.find('div', class_='rstinfo-table__budget')
        
        lunch = landd_tag.find('em', class_='gly-b-lunch')
        dinner = landd_tag.find('em', class_='gly-b-dinner')
        try:
            self.lunch_price = lunch.string
        except:
            self.lunch_price = ''
        try:
            self.dinner_price = dinner.string
        except:
            self.dinner_price = ''
        
        print('　昼：{} 夜：{}'.format(self.lunch_price, self.dinner_price), end='')

        # レビュー一覧URL取得
        #<a class="mainnavi" href="https://tabelog.com/tokyo/A1304/A130401/13143442/dtlrvwlst/"><span>口コミ</span><span class="rstdtl-navi__total-count"><em>60</em></span></a>
        review_tag_id = soup.find('li', id="rdnavi-review")
        review_tag = review_tag_id.a.get('href')

        # レビュー件数取得
        print('  レビュー件数：{}'.format(review_tag_id.find('span', class_='rstdtl-navi__total-count').em.string), end='')
        self.review_cnt = review_tag_id.find('span', class_='rstdtl-navi__total-count').em.string

        # レビュー一覧ページ番号
        page_num = 1 #1ページ*20 = 20レビュー 。この数字を変えて取得するレビュー数を調整。
        self.i = 1
        # レビュー一覧ページから個別レビューページを読み込み、パーシング
        # 店舗の全レビューを取得すると、食べログの評価ごとにデータ件数の濃淡が発生してしまうため、
        # 取得するレビュー数は１ページ分としている（件数としては１ページ*20=20レビュー）
        # COND-0: 全て　COND-1: 昼　COND-2: 夜
        while True:
            review_url_lunch = review_tag + 'COND-1/smp1/?lc=0&rvw_part=all&PG=' + str(page_num)
            # review_url_dinner = review_tag + 'COND-2/smp1/?lc=0&rvw_part=all&PG=' + str(page_num)
            #print('\t口コミ一覧リンク：{}'.format(review_url))
            print(' . ' , end='') #LOG
            if self.scrape_review(review_url_lunch, lunch=True, dinner=False) != True:
                break
            # if self.scrape_review(review_url_dinner, lunch=False, dinner=True) != True:
            #     break
            if page_num >= 20:
                break
            page_num += 1
            

        page_num = 1

        while True:
            #review_url_lunch = review_tag + 'COND-1/smp1/?lc=0&rvw_part=all&PG=' + str(page_num)
            review_url_dinner = review_tag + 'COND-2/smp1/?lc=0&rvw_part=all&PG=' + str(page_num)
            #print('\t口コミ一覧リンク：{}'.format(review_url))
            print(' . ' , end='') #LOG
            # if self.scrape_review(review_url_lunch, lunch=True, dinner=False) != True:
            #     break
            if self.scrape_review(review_url_dinner, lunch=False, dinner=True) != True:
                break
            if page_num >= 20:
                break
            page_num += 1
            


        process_time = time.time() - start
        print('  取得時間：{}'.format(process_time))

        return

    def scrape_review(self, review_url, lunch, dinner):
        """
        レビュー一覧ページのパーシング
        一個ずつReviewの詳細ページを取得
        """
        self.lunch = lunch
        self.dinner = dinner

        try:
            r = requests.get(review_url)
            time.sleep(5)
        except:
            print('Error')
            time.sleep(5)
            return False
        
        if r.status_code != requests.codes.ok:
            print(f'error:not found{ review_url }')
            return False

        # 各個人の口コミページ詳細へのリンクを取得する
        #<div class="rvw-item js-rvw-item-clickable-area" data-detail-url="/tokyo/A1304/A130401/13141542/dtlrvwlst/B408082636/?use_type=0&amp;smp=1">
        #</div>
        # https://tabelog.com/tokyo/A1301/A130101/13070238/dtlrvwlst/COND-0/smp1/?smp=1&lc=0&rvw_part=all
        # https://tabelog.com/tokyo/A1301/A130101/13070238/dtlrvwlst/COND-0/smp1/?smp=1&lc=0&rvw_part=all
        soup = BeautifulSoup(r.content, 'html.parser')
        review_url_list = soup.find_all('div', class_='rvw-item') # 口コミ詳細ページURL一覧

        if len(review_url_list) == 0:
            return False

        for url in review_url_list:
            review_detail_url = 'https://tabelog.com' + url.get('data-detail-url')
            #print('\t口コミURL：', review_detail_url)

            # 口コミのテキストを取得
            self.get_review_text(review_detail_url)
            self.i += 1

        return True

    def get_review_text(self, review_detail_url):
        """
        口コミ詳細ページをパーシング
        """
        r = requests.get(review_detail_url)
        time.sleep(5)
        if r.status_code != requests.codes.ok:
            print(f'error:not found{ review_detail_url }')
            return


        soup = BeautifulSoup(r.content, 'html.parser')

        # 評価の内訳取得
        # 料理味、サービス、雰囲気、CP、酒ドリンク
        points = soup.find('ul', class_='rvw-item__ratings-dtlscore')
        self.points = []
        for li in points.find_all('li'):
            self.points.append(li.strong.text)
        if len(self.points) < 5:
            self.points = ['-', '-', '-', '-', '-']
        self.cuisine = self.points[0]
        self.service = self.points[1]
        self.atmos = self.points[2]
        self.cp = self.points[3]
        self.drink = self.points[4]
        #print('\n料理: {} サービス: {} 雰囲気: {} CP: {} 酒: {}'.format(self.cuisine, self.service, self.atmos, self.cp, self.drink), end='')

        score_tag = soup.find('p', class_='rvw-item__single-ratings-total')
        score = score_tag.b.string
        print(' 口コミ評価点数：{}点'.format(score))
        self.score = score

        # 評価点数が存在しない店舗は除外
        # if score == '-':
        #     print('  評価がないため処理対象外')
        #     self.store_id_num -= 1
        #     return
        
        print("{}個めの口コミ取得完了".format(self.i))
        # Review取得
        review = soup.find_all('div', class_='rvw-item__rvw-comment')#reviewが含まれているタグの中身をすべて取得
        if len(review) == 0:
            review = ''
        else:
            review = review[0].p.text.strip() # strip()は改行コードを除外する関数
            # reviewの1回目訪問のみ取得、複数取得するためにはfor i in range(len(review))でいけるはず...

        #print('\t\t口コミテキスト：', review)
        #self.review = review
        if self.lunch:
            self.lunch_review = review
            self.dinner_review = ''
        
        if self.dinner:
            self.lunch_review = ''
            self.dinner_review = review

        # データフレームの生成
        self.make_df()
        return

    def make_df(self):
        self.store_id = str(self.store_id_num).zfill(8) #0パディング
        se = pd.Series([self.store_id, self.store_name, self.store_score, self.ward, self.lunch_price, self.dinner_price, self.cuisine, self.service, self.atmos, self.cp, self.drink, self.review_cnt, self.score, self.lunch_review, self.dinner_review], self.columns) # 行を作成
        self.df = self.df.append(se, self.columns) # データフレームに行を追加
        return

tokyo_ramen_review = Tabelog(base_url="https://tabelog.com/tokyo/rstLst/sushi/",test_mode=True, pretest=True, p_ward='東京都内')
#CSV保存
tokyo_ramen_review.df.to_csv("../output/detail_tokyo_sushi_review_test.csv")
