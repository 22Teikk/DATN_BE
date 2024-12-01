import uuid
import streamlit as st
import pandas as pd
import numpy as np
import os

from src.domain.entities.utils import get_new_uuid
from src.pages.utils import create_form_from_object
from src.pages.container import repository_container
from src.containers.user_profile_container import UserProfileContainer

user_container = UserProfileContainer(repository_container)

st.write("## Employee")

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
