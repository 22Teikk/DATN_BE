import uuid
import streamlit as st
import pandas as pd
import numpy as np
import os

from src.domain.entities.utils import get_new_uuid
from src.pages.utils import create_form_from_object
from src.pages.container import repository_container
from src.containers.user_profile_container import UserProfileContainer
from src.containers.order_container import OrderContainer
from src.containers.order_item_container import OrderItemContainer
from src.domain.schemas.order_schema import OrderSchema
from src.domain.schemas.order_item_schema import OrderItemSchema
from src.domain.schemas.user_profile_schema import UserProfileSchema

user_container = UserProfileContainer(repository_container)
order_container = OrderContainer(repository_container)
order_item_container = OrderItemContainer(repository_container)
st.write("## Customer")

orders_data = OrderSchema().dump(order_container.usecase.find_by_query(), many=True)
order_items_data = OrderItemSchema().dump(order_item_container.usecase.find_by_query(), many=True)
users_data = UserProfileSchema().dump(user_container.usecase.find_by_query({"role_id": "1"}), many=True)
def load_user_data():
    data = user_container.usecase.find_by_query({"role_id": "1"})
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
    st.session_state.dek = str(uuid.uuid4()) 

if 'dek' not in st.session_state:
    st.session_state.dek = str(uuid.uuid4())
if 'df_app' not in st.session_state:
    load_user_data()

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


import plotly.figure_factory as ff
import plotly.express as px

col1, col2 = st.columns(2)

def load_user_order_most():
    users_df = pd.DataFrame(users_data)
    orders_df = pd.DataFrame(orders_data)

    # Kết hợp dữ liệu User và Order dựa trên khóa ngoại user_id
    merged_df = orders_df.merge(users_df, left_on="user_id", right_on="_id", how="inner")

    # Thống kê số lượng đơn hàng theo từng người dùng
    order_count = merged_df.groupby(["user_id", "name"])["_id_x"].count().reset_index()

    # Đổi tên cột cho dễ hiểu
    order_count.rename(columns={"_id_x": "order_count"}, inplace=True)

    # Sắp xếp theo số lượng đơn hàng giảm dần
    order_count = order_count.sort_values(by="order_count", ascending=False)
    
    st.write("## Users with the Most Orders")
    st.write(order_count)

def load_user_order_cost():
    users_df = pd.DataFrame(users_data)
    orders_df = pd.DataFrame(orders_data)
    order_items_df = pd.DataFrame(order_items_data)

    # Bước 1: Kết hợp dữ liệu
    # Kết hợp OrderItem với Order để lấy thông tin user_id
    order_items_with_user = order_items_df.merge(orders_df, left_on="order_id", right_on="_id", how="inner")

    # Kết hợp tiếp với User để lấy thông tin người dùng
    order_items_with_user = order_items_with_user.merge(users_df, left_on="user_id", right_on="_id", how="inner")

    # Bước 2: Tính tổng tiền cho từng OrderItem
    order_items_with_user["total_price"] = order_items_with_user["quantity"] * order_items_with_user["price"]

    # Bước 3: Tính tổng tiền mua hàng theo từng người dùng
    user_total_spending = order_items_with_user.groupby(["user_id", "name"])["total_price"].sum().reset_index()

    # Đổi tên cột cho dễ hiểu
    user_total_spending.rename(columns={"total_price": "total_spent"}, inplace=True)

    # Sắp xếp theo tổng tiền giảm dần
    user_total_spending = user_total_spending.sort_values(by="total_spent", ascending=False)
    st.write("## User Spending Amount")
    st.write(user_total_spending)

edited_df = st.data_editor(
    st.session_state.df_app,
    num_rows="dynamic",
    use_container_width=True,
    disabled=["_id"],
    key=st.session_state.dek,
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


load_user_order_most()
load_user_order_cost()
