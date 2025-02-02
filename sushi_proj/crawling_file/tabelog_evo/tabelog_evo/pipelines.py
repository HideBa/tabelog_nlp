# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import psycopg2
import logging
# 値のバリデーションチェック


class ValidationPipeline(object):
    def process_item(self, item: scrapy.Item, spider: scrapy.Spider):
        # if (item['lunch_review'] is None or item['lunch_review'] == '') and (item['dinner_review'] is None or item['dinner_review'] == ''):
        #     raise scrapy.exceptions.DropItem('Missing value: review')

        if (item['review'] is None or item['review'] == ''):
            raise scrapy.exceptions.DropItem('Missing value: review')

        if item['store_score'] is None or item['store_score'] == '-':
            raise scrapy.exceptions.DropItem('Missing value: store_score')

        return item

# PostgreSQLへの保存


class PostgresPipeline(object):
    def open_spider(self, spider: scrapy.Spider):
        # コネクションの開始
        url = spider.settings.get('POSTGRESQL_URL')
        self.conn = psycopg2.connect(url)

    def close_spider(self, spider: scrapy.Spider):
        # コネクションの終了
        self.conn.close()

    def process_item(self, item: scrapy.Item, spider: scrapy.Spider):
        curs = self.conn.cursor()
        # Store テーブル
        store_col = "(id, store_name, tabelog_score, station, lunch_price, dinner_price, address, \
                    phone_num, opening_time, regular_holiday, url, latitude, longitude, retty_score)"
        store_sql = "INSERT INTO store {} VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)".format(
            store_col)

        # store_idが既にある場合はStoreテーブルに入れずにreturn
        store_id = item['store_id']
        curs.execute(
            'SELECT * FROM sushi_app_store WHERE (id = %s)', (store_id,))
        record = curs.fetchone()
        if record is not None:
            logging.info(
                'id is already registered. id:%s' %
                (id,))
            return item

        # Tableに追加
        curs.execute(
            store_sql,
            (item['store_id'],
             item['store_name'],
                item['store_score'],
                item['station'],
                item['lunch_price'],
                item['dinner_price'],
                item['address'],
                item['phone_num'],
                item['opening_time'],
                item['regular_holiday'],
                item['url'],
                item['latitude'],
                item['longitude'],
                0))
        self.conn.commit()

        # Review テーブル
        review_col = "(score, store_id, id, content, user_sex, is_new)"
        review_sql = "INSERT INTO sushi_app_Review {} VALUES (%s, %s, %s, %s, %s, %s)".format(
            review_col)
        is_new = True
        curs.execute(
            review_sql,
            (item['score'],
             item['store_id'],
                item['ld_id'],
                item['review'],
                item['gender'],
                is_new))
        self.conn.commit()

        return item


class RettyPipeline(object):
    def open_spider(self, spider: scrapy.Spider):
        # コネクションの開始
        url = spider.settings.get('POSTGRESQL_URL')
        self.conn = psycopg2.connect(url)

    def close_spider(self, spider: scrapy.Spider):
        # コネクションの終了
        self.conn.close()

    def process_item(self, item: scrapy.Item, spider: scrapy.Spider):
        curs = self.conn.cursor()

        col = "(name, phone_num, retty_score)"
        sql = "INSERT INTO sushi_app_retty {} VALUES (%s, %s, %s)".format(col)

        # storeに同じ電話番号があれば処理開始
        phone_num = item['phone_num']
        curs.execute(
            'SELECT * FROM store WHERE (phone_num = %s)', (phone_num,))
        record = curs.fetchone()
        if record is not None:
            curs.execute(
                sql,
                (item['name'],
                 item['phone_num'],
                    item['wannago']))
            self.conn.commit()

            # storeにアップデート
            store_sql = "UPDATE store SET retty_score = %s WHERE (phone_num = %s)"
            curs.execute(store_sql, (item['wannago'], item['phone_num']))
            self.conn.commit()
            return item
