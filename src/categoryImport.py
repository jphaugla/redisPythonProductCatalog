import xml.etree.ElementTree as ET
import redis

REDIS_HOST = 'localhost'


def main():
    conn = redis.Redis('localhost')
    with open('../data/CategoriesList.xml') as xml_file:
        # create element tree object
        tree = ET.parse(xml_file)

        # get root element
        root = tree.getroot()
        print("root.tag is ", root.tag)
        for child in root:
            print("child tag is " + child.tag)
            print("child attribute is " + str(child.attrib))
        cat_idx = 0
        pipe = conn.pipeline()
        for cat in root.findall('Response/CategoriesList/Category'):
            # print("starting in xml file")
            # print("cat.tag is " + str(cat.tag))
            # print("cat.attribute is " + str(cat.attrib))

            cat_id = cat.attrib['ID']
            # print("ID is ", str(cat_id))

            cat_idx += 1
            category_id = 'categ:' + cat_id
            conn.hset(category_id, "ID", cat_id)
            if cat.attrib['LowPic']:
                pipe.hset(category_id, "lowpic", cat.attrib['LowPic'])
            if cat.attrib['ThumbPic']:
                pipe.hset(category_id, "thumbpic", cat.attrib['ThumbPic'])
            for cat_child in cat:
                # category_id is
                # print("cat_child.tag is " + str(cat_child.tag))
                # print("cat_child.attribute is " + str(cat_child.attrib))
                if cat_child.tag == 'Name' and cat_child.attrib['langid'] == '1':
                    cat_name = cat_child.attrib['Value']
                    # print("category name is " + cat_name)
                    pipe.hset(category_id, "Name", cat_name)
            if cat_idx % 200 == 0:
                pipe.execute()
                if cat_idx % 1000 == 0:
                    print(str(cat_idx) + " categories loaded")

    xml_file.close()
    print(str(cat_idx) + " categories loaded")


if '__main__' == __name__:
    main()
