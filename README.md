# redisPythonProductCatalog
A simple product catalog solution based on icecat files
#  installing python on mac
1. install xcode
2. install homebrew
```bash
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
3. verify homebrew
```bash
brew doctor
```
4. install python
```bash
brew install python
```
5. install redis-py
```bash
pip install redis
```
6.  install flask
```bash
pip install flask
```
6. clone repository
```bash
git clone https://github.com/jphaugla/redisPythonProductCatalog.git
```
7. install redis
```bash
brew install redis
```
8. start redis 
	redis-server /usr/local/etc/redis.conf

## Code and File discussion
This is an implementation of a product Catalog using data download from
 [icecat](https://iceclog.com/open-catalog-interface-oci-open-icecat-xml-and-full-icecat-xml-repositories/)
Unzip the data files
```bash
cd redis_python/productCat/data
unzip files.index.csv.zip
gunzip CategoriesList.xml.gz
```
  * load categories
```bash
python3 ./src/categoryImport.py
```
  * load Products
```bash
python3 ./src/productImport.py
```
  * start flask app server
This only works with python2-hopefully can fix the bug soon
 ```bash
 python2 ./src/appy.py
 ```
  * run API tests
Note:  there are multiple API tests in the file but only one should be run at a time
So, the tests not to be run should be commented out.
 ```bash
./scripts/sampleput.sh
```