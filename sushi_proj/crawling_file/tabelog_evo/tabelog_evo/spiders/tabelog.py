# -*- coding: utf-8 -*-
import scrapy
import requests
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
from tabelog_evo.items import TabelogEvoItem


class TabelogSpider(CrawlSpider):
    """
    食べログスクレイピングスパイダー
    東京の寿司屋さんの口コミををスクレイピングする
    """
    store_id = 0
    page_num = 1
    name = 'tabelog'
    allowed_domains = ['tabelog.com']
    start_urls = [
        'https://tabelog.com/tokyo/rstLst/sushi/?Srt=D&SrtT=rt&sort_mode=1']
    custom_settings = {
        "SPIDER_MIDDLEWARES": {
            'scrapy_crawl_once.CrawlOnceMiddleware': 100,
        },
        "DOWNLOADER_MIDDLEWARES": {
            'scrapy_crawl_once.CrawlOnceMiddleware': 50,
        },
        "ITEM_PIPELINES": {
            'tabelog_evo.pipelines.ValidationPipeline': 300,
            'tabelog_evo.pipelines.PostgresPipeline': 600
        },
    }

    def parse(self, response):
        """
        start_urlsに対する処理
        各お店の口コミページに移行
        """
        url_list = response.css(
            'a.list-rst__rvw-count-target').xpath('@href').getall()
        # Reviewが15件以下なら除外
        review_cnt_list = response.css(
            'a.list-rst__rvw-count-target em').xpath("string()").getall()
        # for url in url_list[:2]:
        count = 0
        for url, review_cnt in zip(url_list, review_cnt_list):
            count += 1
            if count > 20:
                break
            item = TabelogEvoItem()
            if int(review_cnt) <= 15:
                return
            store_url = response.css(
                'a.list-rst__rst-name-target::attr("href")').get()
            item['url'] = store_url
            self.store_id += 1
            item['store_id'] = self.store_id
            request = scrapy.Request(
                url,
                callback=self.parse_review
            )
            request.meta['item'] = item
            yield request

        # 次ページに移行
        next_page = response.css(
            'a.c-pagination__arrow--next').xpath('@href').get()
        if next_page is not None and self.page_num < 1:
            self.page_num += 1
            href = response.urljoin(next_page)
            request = scrapy.Request(href, callback=self.parse)
            request.meta['item'] = item
            yield request

    def parse_detail(self, response):
        """
        店の詳細ページのパーシング
        口コミページに移行
        """
        item = response.meta['item']

        # 店舗名取得
        soup = BeautifulSoup(response.body, 'html.parser')
        store_name_tag = soup.find('h2', class_='display-name')
        store_name = store_name_tag.span.string
        print('{}→店名：{}'.format(self.store_id, store_name.strip()), end='')
        item['store_name'] = store_name.strip()

        # お寿司屋以外を除外
        store_head = soup.find(
            'div', class_='rdheader-subinfo')  # 店舗情報のヘッダー枠データ取得
        store_head_list = store_head.find_all('dl')
        store_head_list = store_head_list[1].find_all('span')

        if store_head_list[0].text not in {'寿司'}:
            print('お寿司屋さんではないので処理対象外')
            self.store_id -= 1
            return

        # 評価点数取得
        rating_score_tag = soup.find('b', class_='c-rating__val')
        rating_score = rating_score_tag.span.string
        print('  評価点数：{}点'.format(rating_score), end='')
        item['store_score'] = rating_score

        # 昼夜の価格帯を取得
        # landd_tag = soup.find('div', class_='rstinfo-table__budget')

        # lunch = landd_tag.find('em', class_='gly-b-lunch')
        # dinner = landd_tag.find('em', class_='gly-b-dinner')
        # try:
        #     item['lunch_price'] = lunch.string
        # except:
        #     item['lunch_price'] = ''
        # try:
        #     item['dinner_price'] = dinner.string
        # except:
        #     item['dinner_price'] = ''

        #print('　昼：{} 夜：{}'.format(self.lunch_price, self.dinner_price), end='')

        # レビュー一覧URL取得
        review_tag_id = soup.find('li', id="rdnavi-review")
        review_tag = review_tag_id.a.get('href')

        # レビュー件数取得
        print(
            '  レビュー件数：{}'.format(
                review_tag_id.find(
                    'span',
                    class_='rstdtl-navi__total-count').em.string))
        #item['review_cnt'] = review_tag_id.find('span', class_='rstdtl-navi__total-count').em.string

        request = scrapy.Request(
            review_tag,
            callback=self.parse_review
        )
        request.meta['item'] = item
        yield request

    def parse_review(self, response):
        """
        口コミ一覧ページのパーシング
        口コミ詳細ページに移行
        """
        item = response.meta['item']

        # ジャンルが寿司ではなかったら除外
        genre = response.css(
            'div.rdheader-subinfo dl span').xpath('string()').getall()[1]
        if genre != '寿司':
            self.store_id -= 1
            return

        # 店名取得
        store_name = response.css(
            'h2.display-name').xpath('string()').get().strip()
        item['store_name'] = store_name

        # お店のスコア取得
        store_score = response.css(
            'b.rdheader-rating__score-val span').xpath('string()').get()
        item['store_score'] = store_score

        # 最寄り駅取得
        station = response.css('dt:contains("最寄り駅")+dd span::text').get()
        item['station'] = station

        # 昼夜の価格帯取得
        lunch_price = response.css(
            'p.rdheader-budget__icon--lunch a::text').get()
        dinner_price = response.css(
            'p.rdheader-budget__icon--dinner a::text').get()
        item['lunch_price'] = lunch_price
        item['dinner_price'] = dinner_price

        # 住所取得
        address = response.css(
            '.rstinfo-table__address').xpath('string()').get().strip()
        item['address'] = address

        # 電話番号取得
        phone_num = response.css(
            '.rstinfo-table__tel-num-wrap').xpath('string()').get().strip()
        item['phone_num'] = phone_num

        # 営業時間取得
        time = response.css('th:contains("営業時間・")+td p::text').getall()

        # このままでは定休日も含まれているのでindexを取得し、スライス
        index_holi = time.index('定休日')
        # ['営業時間', '月曜日', '火曜日', '定休日', '水曜日']
        opening = time[1:index_holi]
        holiday = time[index_holi + 1:]
        item['opening_time'] = '\n'.join(opening)
        item['regular_holiday'] = '\n'.join(holiday)

        # Google Static Mapsの画像urlからお店の緯度経度取得
        latitude, longitude = response.css(
            'img.js-map-lazyload::attr("data-original")').re(r'markers=.*?%7C([\d.]+),([\d.]+)')
        item['latitude'] = latitude
        item['longitude'] = longitude

        # 口コミ詳細ページURL一覧
        review_url_list = response.css(
            'div.rvw-item').xpath('@data-detail-url').getall()

        # レヴュー0件のお店は除く
        if len(review_url_list) == 0:
            return

        # 各口コミの詳細ページに移行
        for url in review_url_list:
            review_detail_url = response.urljoin(url)
            request = scrapy.Request(
                review_detail_url,
                callback=self.get_review_text
            )
            request.meta['item'] = item
            #request.meta['crawl_once'] = True
            yield request

        # 次ページ
        # next_page = response.css('a.c-pagination__arrow--next').xpath('@href').get()
        # if next_page is not None:
        #     href = response.urljoin(next_page)
        #     request = scrapy.Request(href, callback=self.parse_review)
        #     request.meta['item'] = item
        #     yield request

    def get_review_text(self, response):
        """
        口コミ詳細ページのパーシング
        その人の口コミを全て収集
        """
        item = response.meta['item']

        # 性別を取得　0:　男性　1: 女性　2: 不明
        gender = response.css('span.rvw-item__rvwr-profile').re('.性')
        if '男性' in gender:
            item['gender'] = 0
        elif '女性' in gender:
            item['gender'] = 1
        else:
            item['gender'] = 2

        # 各口コミの時間帯、スコア、詳細、本文を取得する
        # 時間帯のリスト　dinner: or lunch:
        time_list = response.css('strong.c-rating__time::text').getall()
        # 口コミのスコアリスト 5.0など
        score_list = response.css(
            'p.c-rating.rvw-item__single-ratings-total > b.c-rating__val.c-rating__val--strong::text').getall()
        # 評価の内訳　5個ずつ格納
        dtl_tag = response.css(
            'ul.rvw-item__single-ratings-dtlscore li strong::text').getall()
        dtl_list = [dtl_tag[x:x + 5] for x in list(range(0, len(dtl_tag), 5))]
        # 本文の取得
        # 「おすすめポイント」は口コミではないので除く
        review_list = response.css(
            'div.rvw-item__rvw-comment p').xpath('string()').getall()
        recommend = response.css(
            'div.rvw-item__review-contents--recommend').getall()
        if recommend:
            review_list = review_list[len(recommend) * 2:]
        # 時間帯、スコア、詳細には下部の余分なものも含まれているため、除く
        cnt = len(review_list)
        for time, score, detail, review in zip(
                time_list[:cnt], score_list[:cnt], dtl_list[:cnt], review_list):
            if score == '-':
                score = 0
            item['score'] = score
            item['detail'] = detail
            if time == 'lunch:' or time == '昼:':
                # item['lunch_review'] = review
                # item['dinner_review'] = ''
                item['ld_id'] = 0

            elif time == 'dinner:' or time == '夜:':
                # item['lunch_review'] = ''
                # item['dinner_review'] = review
                item['ld_id'] = 1
            item['review'] = review
            yield item
