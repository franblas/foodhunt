# -*- coding: utf-8 -*-

import rethinkdb as r
import time

DB_HOST = 'localhost'
DB_PORT = 28015

class Database(object):

    def __init__(self, db):
        self.db = db
        self.con = self.connect(database=db)

    def connect(self, database):
        max_try = 3
        nb_try = 0
        while nb_try < max_try:
            try:
                return r.connect(host=DB_HOST, port=DB_PORT, db=database)
            except:
                nb_try += 1
                time.sleep(2)
            if nb_try == max_try:
                raise Exception('Cannot connect to database ' + DB_HOST + ':' + str(DB_PORT))

    def insert_product(self, collection, doc):
        product_id = r.table(collection).insert(doc).run(self.con)
        return product_id

    def close(self):
        self.con.close()
