from sqlalchemy import Column, Integer, String, create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoSuchTableError, InvalidRequestError
from config import Config
from src.domain.entities.utils import Base

class MySQL:
    def __init__(self):
        try:
            self.engine = create_engine(f"mysql+pymysql://{Config.MYSQL_USERNAME}:{Config.MYSQL_PASSWORD}@{Config.MYSQL_HOST}:{Config.MYSQL_PORT}/{Config.MYSQL_DB}", pool_pre_ping=True,  # Đảm bảo kiểm tra kết nối trước khi sử dụng
                pool_recycle=3600)
            Session = sessionmaker(bind=self.engine)
            self.session = Session()

            print(">>> Kết nối tới MySQL thành công!")
        except Exception as e:
            print(">>> Không thể kết nối tới MySQL.", e)
            exit(1)

    def get_session(self):
        if not self._is_session_valid():
            self._reset_session()
        return self.session

    def _is_session_valid(self) -> bool:
        """Kiểm tra trạng thái của phiên làm việc."""
        try:
            self.session.execute("SELECT 1")  # Kiểm tra xem kết nối có hoạt động không
            return True
        except InvalidRequestError:
            return False
        except Exception as e:
            return False

    def _reset_session(self):
        """Đóng phiên làm việc hiện tại và tạo một phiên mới."""
        try:
            self.session.close()  # Đóng phiên làm việc hiện tại
        except Exception as e:
            print(f">>> Lỗi khi đóng session: {e}")
        finally:
            Session = sessionmaker(bind=self.engine)
            self.session = Session()  # Tạo phiên làm việc mới

    def get_table(self, table_name, model: type):
        meta = MetaData()

        try:
            # Tự động ánh xạ bảng từ database
            table = Table(table_name, meta, autoload_with=self.engine)
            return table
        except NoSuchTableError:

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