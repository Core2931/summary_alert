from datetime import datetime
from module.mongoDB.get_mongodb import get_data_mongo

def main():
    try:
        get_data_mongo()
    except Exception as e:
        print(e)

main()