from sqlalchemy import Column, Integer, String, create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoSuchTableError
from config import Config
from src.domain.entities.utils import Base

class MySQL:
    def __init__(self):
        try:
            self.engine = create_engine(f"mysql+pymysql://{Config.MYSQL_USERNAME}:{Config.MYSQL_PASSWORD}@{Config.MYSQL_HOST}:{Config.MYSQL_PORT}/{Config.MYSQL_DB}")
            Session = sessionmaker(bind=self.engine)
            self.session = Session()

            print(">>> Kết nối tới MySQL thành công!")
        except Exception as e:
            print(">>> Không thể kết nối tới MySQL.", e)
            exit(1)

    def get_session(self):
        return self.session

    def get_table(self, table_name, model: type):
        meta = MetaData()

        try:
            # Tự động ánh xạ bảng từ database
            table = Table(table_name, meta, autoload_with=self.engine)
            print(f">>> Bảng '{table_name}' đã được ánh xạ thành công.")
            return table
        except NoSuchTableError:
            print(f">>> Bảng '{table_name}' không tồn tại trong cơ sở dữ liệu. Đang tạo mới bảng...")

            # Xử lý rollback nếu có lỗi trong giao dịch trước đó
            try:
                self.session.rollback()  # Rollback giao dịch nếu có lỗi
            except Exception as e:
                print(f">>> Lỗi khi rollback: {e}")

            # Tạo bảng mới nếu nó không tồn tại
            self.create_table(table_name, model)
            # Lấy lại bảng sau khi tạo
            table = Table(table_name, meta, autoload_with=self.engine)
            return table

    def create_table(self, table_name, model):
        # Kiểm tra xem mô hình có phải là lớp hay không
        if not isinstance(model, type) or not issubclass(model, Base):
            raise ValueError("Mô hình phải là một lớp con của Base.")

        # Thiết lập tên bảng
        model.__tablename__ = table_name
        
        # Tạo bảng mới
        Base.metadata.create_all(self.engine)
        print(f">>> Bảng '{table_name}' đã được tạo thành công.")