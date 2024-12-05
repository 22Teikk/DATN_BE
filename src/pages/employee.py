import uuid
import streamlit as st
import pandas as pd
import numpy as np
import os

from src.domain.entities.utils import get_new_uuid
from src.pages.utils import create_form_from_object
from src.pages.container import repository_container
from src.containers.user_profile_container import UserProfileContainer
from src.containers.working_container import WorkingContainer
from src.containers.order_container import OrderContainer

from src.domain.schemas.user_profile_schema import UserProfileSchema 
from src.domain.schemas.order_schema import OrderSchema 
from src.domain.schemas.working_schema import WorkingSchema 

user_container = UserProfileContainer(repository_container)
order_container = OrderContainer(repository_container)
working_container = WorkingContainer(repository_container)

@st.cache_data(ttl=60)
def load_data():
    st.session_state.users_data = UserProfileSchema().dump(user_container.usecase.find_by_query(), many=True)
    st.session_state.workings_data = working_container.usecase.find_by_query()
    st.session_state.orders_data = OrderSchema().dump(order_container.usecase.find_by_query() , many=True)

# Lấy dữ liệu ứng dụng
def load_user_data():
    data = user_container.usecase.find_by_query({"role_id": "2"})
    df = pd.DataFrame.from_dict(data)
    
    if not df.empty:
        # Kiểm tra nếu cột 'Select' chưa tồn tại, nếu chưa thì thêm vào
        if "Select" not in df.columns:
            df.insert(0, "Select", False)  # Thêm cột checkbox vào vị trí đầu tiên
        else:
            # Nếu cột 'Select' đã tồn tại nhưng không ở đầu, đưa nó về đầu
            select_col = df.pop("Select")
            df.insert(0, "Select", False)  # Đảm bảo cột 'Select' ở vị trí đầu tiên
        
    st.session_state.df_app = df
    st.session_state.dek_employee = str(uuid.uuid4()) 
    load_data()

if 'dek_employee' not in st.session_state:
    st.session_state.dek_employee = str(uuid.uuid4())
if 'df_app' not in st.session_state:
    load_user_data()
if 'users_data' or 'workings_data' or 'orders_data' not in st.session_state:
    load_data()

def delete_rows():
    edited_df["Select"] = edited_df["Select"].fillna(False)
    # Lọc các dòng được chọn
    selected_rows = edited_df[edited_df["Select"]]
    if selected_rows.empty:
        st.warning("No rows selected")
    else:
        for row in selected_rows.to_dict("records"):
            user_container.usecase.delete(row["_id"])  # Xóa trong DB
        load_user_data()

def save_records():
    # Chuẩn bị dữ liệu để lưu
    records = edited_df.drop(columns=["Select"]).to_dict("records")  # Bỏ cột Select
    for record in records:
        if "_id" not in record or not record["_id"] or np.isnan(record["_id"]):
            record["_id"] = get_new_uuid()  # Tự sinh `_id` nếu chưa có
    user_container.usecase.upserts(records)  # Lưu dữ liệu vào DB

def load_employee_performance():
    users_df = pd.DataFrame(st.session_state.users_data)
    workings_df = pd.DataFrame(st.session_state.workings_data)
    orders_df = pd.DataFrame(st.session_state.orders_data)

    # Bước 1: Kết hợp Working với Order dựa trên order_id
    workings_with_order = workings_df.merge(orders_df, left_on="order_id", right_on="_id", how="inner")
    employee_order = workings_with_order.merge(users_df, left_on="user_id_x", right_on="_id", how="inner")
    # Bước 2: Chuyển đổi cột created_at thành kiểu datetime để dễ dàng lọc theo ngày, tháng, năm
    employee_order["date"] = pd.to_datetime(employee_order["date"])

    # Bước 3: Thêm lựa chọn lọc theo ngày, tháng hoặc năm
    time_filter = st.selectbox("Select Time Filter", ["Day", "Month", "Year"])

    # Bước 4: Lọc dữ liệu theo thời gian
    if time_filter == "Day":
        employee_order["date"] = employee_order["date"].dt.date
    elif time_filter == "Month":
        employee_order["date"] = employee_order["date"].dt.to_period('M')
    elif time_filter == "Year":
        employee_order["date"] = employee_order["date"].dt.to_period('Y')

    # Bước 5: Nhóm theo tên nhân viên và lọc theo thời gian
    order_count_per_employee = employee_order.groupby(["name", "date"])["order_id"].count().reset_index()

    # Đổi tên cột cho dễ hiểu
    order_count_per_employee.rename(columns={"order_id": "order_count"}, inplace=True)

    # Bước 6: Sắp xếp theo số lượng đơn hàng giảm dần
    order_count_per_employee = order_count_per_employee.sort_values(by="order_count", ascending=False)

    # Bước 7: Hiển thị kết quả
    st.write(f"## Employees with the Most Orders ({time_filter})")
    st.write(order_count_per_employee)

import plotly.figure_factory as ff
import plotly.express as px

col1, col2 = st.columns(2)

load_employee_performance()

st.write("## Employees Table")
edited_df = st.data_editor(
    st.session_state.df_app,
    num_rows="dynamic",
    use_container_width=True,
    disabled=["_id"],
    key=st.session_state.dek_employee,
)

# Các nút chức năng
c1, c2, c3 = st.columns(3)

# Nút Reset
with c1:
    st.button("Reset", on_click=load_user_data ,use_container_width=True, type="secondary")

# Nút Delete
with c2:
    st.button("Delete", on_click=delete_rows, use_container_width=True, type="secondary")
 
# Nút Save Change
with c3:
    st.button("Save Change", on_click=save_records, use_container_width=True, type="primary")
