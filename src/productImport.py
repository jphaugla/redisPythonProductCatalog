import csv
import redis
import sys
maxInt = sys.maxsize


REDIS_HOST = 'localhost'


def main():
    conn = redis.Redis('localhost')
    #  open the file to read as csv
    with open('../data/files.index.csv') as csv_file:
        # file is tab delimited
        csv_reader = csv.reader(csv_file, delimiter='\t', quoting=csv.QUOTE_NONE)
        prod_idx = 0
        fields = next(csv_reader, None)
        #  go through all rows in the file
        for row in csv_reader:
            #  increment prod_idx and use as incremental part of the key
            prod_idx += 1
            # hash key
            # print("prodid " + prodid )
            # 0)path 1)product_id 2)updated 3)quality 4)supplier_id 5)prod_id 6)catid 7)m_prod_id 8)ean_upc 9)on_market
            # 10)country_market 11)model_name 12)product_view 13)high_pic 14)high_pic_size 15)high_pic_width 16)high_pic_height
            # 17)m_supplier_id 18)m_supplier_name 19)ean_upc_is_approved 20)Limited Date_Added
            col_idx = 0
            pipe = conn.pipeline()
            for col in row:
                # print("column hdr " + fields[col_idx])
                # print("column value " + col)
                # alternative product keys
                #  hash key is prod string with prod_id and finally supplier_id
                # hash_key = "prod:" + row[5] + ":" + row[4]
                #  hash key is prod string with m_supplier_name and finally prod_id
                # hash_key = "prod:" + row[18] + ":" + row[5]
                #  hash key is prod string with sequential id
                hash_key = "prod:" + str(prod_idx)
                if col and not col.isspace():
                    pipe.hset(hash_key, fields[col_idx], col)
                    # index will be model name and hold value of prod_idx
                    index_value = str(row[11]) + ":" + str(prod_idx)
                    pipe.zadd("zProdModelName", {index_value: 0})
                col_idx += 1
            if prod_idx % 100 == 0:
                pipe.execute()
                if prod_idx % 10000 == 0:
                    print(str(prod_idx) + " rows loaded")
        csv_file.close()
        print(str(prod_idx) + " rows loaded")


if '__main__' == __name__:
    main()
