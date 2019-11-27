import csv
import redis
import sys

from redis.client import Pipeline

maxInt = sys.maxsize


REDIS_HOST = 'redis'


def main():
    # global redis_pool
    # print("PID %d: initializing redis pool..." % os.getpid())
    # redis_pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
    conn = redis.StrictRedis(host=REDIS_HOST, port=6379, db=0, charset="utf-8", decode_responses=True)
    pipe = conn.pipeline()
    #  open the file to read as csv
    with open('/data/files.index.csv') as csv_file:
        # file is tab delimited
        csv_reader = csv.reader(csv_file, delimiter='\t', quoting=csv.QUOTE_NONE)
        prod_idx = 0
        fields = next(csv_reader, None)
        #  go through all rows in the file
        for row in csv_reader:
            #  increment prod_idx and use as incremental part of the key
            prod_idx += 1
            hash_key = "prod:" + str(prod_idx)
            # print("hash_key is " + hash_key)
            # hash key
            # print("prodid " + prodid )
            # 0)path 1)product_id 2)updated 3)quality 4)supplier_id 5)prod_id 6)catid 7)m_prod_id 8)ean_upc 9)on_market
            # 10)country_market 11)model_name 12)product_view 13)high_pic 14)high_pic_size
            # 15)high_pic_width 16)high_pic_height 17)m_supplier_id 18)m_supplier_name 19)ean_upc_is_approved
            # 20)Limited Date_Added
            # index will be model name and hold value of prod_idx
            index_value = str(row[11]) + ":" + str(prod_idx)
            # print("index value is " + index_value)
            pipe.zadd("zProdModelName", {index_value: 0})
            # this index will be category_ID per product
            category_set = "zCategProd:" + str(row[6])
            # print("category name is " + category_set)
            pipe.zadd(category_set, {hash_key: 0})
            # add the category name  ****  WARNING *****  the category name breaks pipelining
            # category_id = 'categ:' + row[6]
            # categ_name = conn.hget(category_id, "Name")
            # print("category name is " + str(categ_name))
            # conn.hset(hash_key, "cat_name", str(categ_name))
            col_idx = 0
            for col in row:
                # print("column hdr " + fields[col_idx])
                # print("column value " + col)
                # alternative product keys
                #  hash key is prod string with prod_id and finally supplier_id
                # hash_key = "prod:" + row[5] + ":" + row[4]
                #  hash key is prod string with m_supplier_name and finally prod_id
                # hash_key = "prod:" + row[18] + ":" + row[5]
                #  hash key is prod string with sequential id
                if col and not col.isspace():
                    pipe.hset(hash_key, fields[col_idx], col)
                col_idx += 1
            if prod_idx % 100 == 0:
                pipe.execute()
                if prod_idx % 10000 == 0:
                    print(str(prod_idx) + " rows loaded")
        csv_file.close()
        print(str(prod_idx) + " rows loaded")
        pipe.set("prod_highest_idx", prod_idx)
        pipe.execute()


if '__main__' == __name__:
    main()
