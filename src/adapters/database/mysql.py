from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker

class MySQL:
    def __init__(self):
        try:
            self.engine = create_engine("mysql+pymysql://root:kietnt@94.237.64.46:3306")
            
            Session = sessionmaker(bind=self.engine)
            self.session = Session()

            print(">>> Kết nối tới MySQL thành công!")
        except Exception as e:
            print(">>> Không thể kết nối tới MySQL.", e)
            exit(1)

    def get_table(self, table_name):
        meta = MetaData(self.engine)
        table = Table(table_name, meta, autoload_with=self.engine)
        return table

