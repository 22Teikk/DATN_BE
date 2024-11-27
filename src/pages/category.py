import uuid
import streamlit as st
import pandas as pd
import numpy as np
import os

from src.domain.schemas.category_schema import CategorySchema
from src.domain.entities.category import Category
from src.domain.entities.utils import get_new_uuid
from src.pages.utils import create_form_from_object
from src.pages.container import repository_container
from src.containers.category_container import CategoryContainer
import requests

category_container = CategoryContainer(repository_container=repository_container)

def load_category_data():
    data = category_container.usecase.find_by_query()
    df = pd.DataFrame.from_dict(data)
    
    if not df.empty:
        # Kiểm tra nếu cột 'Select' chưa tồn tại, nếu chưa thì thêm vào
        if "Select" not in df.columns:
            df.insert(0, "Select", False)  # Thêm cột checkbox vào vị trí đầu tiên
        else:
            # Nếu cột 'Select' đã tồn tại nhưng không ở đầu, đưa nó về đầu
            select_col = df.pop("Select")
            df.insert(0, "Select", False)  # Đảm bảo cột 'Select' ở vị trí đầu tiên
        
    st.session_state.df_category = df  # Cập nhật DataFrame trong session state
    st.session_state.dek = str(uuid.uuid4())  # Đổi khóa để làm mới bảng

def delete_rows():
    editor["Select"] = editor["Select"].fillna(False)
    selected_rows = editor[editor["Select"]]
    
    if selected_rows.empty:
        st.warning("No rows selected")
    else:
        for row in selected_rows.to_dict("records"):
            category_container.usecase.delete(row["_id"])  # Xóa trong DB
        st.success("Records deleted successfully.")
        load_category_data()

def save_change():
    records = editor.drop(columns=["Select"]).to_dict("records")  # Bỏ cột Select
    category_container.usecase.upserts(records)  # Lưu dữ liệu vào DB
    load_category_data()
    st.success("Save changes")

if 'dek' not in st.session_state:
    st.session_state.dek = str(uuid.uuid4())
if "show_form" not in st.session_state:
    st.session_state.show_form = False
if 'df_category' not in st.session_state:
    load_category_data()
# Nút để hiển thị form
col1, col2 = st.columns(2)
with col1:
    st.write("Category")
with col2:
    if st.button("Create Category", use_container_width=True, type="primary"):
        st.session_state.show_form = True

# Hiển thị form khi `show_form` là True
if st.session_state.show_form:
    st.write("### Create New Category")

    # Form để nhập thông tin
    with st.form("form_category"):
        name = st.text_input(label="Category Name")
        image = st.file_uploader(
            accept_multiple_files=False,
            label="Select Image",
            type=["png", "jpg", "jpeg", "gif", "webp"],
            key="uploaded_file",  # Đảm bảo trạng thái không bị reset
        )
        submit = st.form_submit_button("Create")

    # Xử lý khi nhấn submit
    if submit:
        if image is not None and name is not None:
            # Chuẩn bị file để upload
            files = {
                'file': (image.name, image.getvalue(), image.type)
            }
            url = f"{os.getenv('APP_HOST')}/upload"
            response = requests.post(url, files=files)
            category = Category(
                get_new_uuid(),
                name,
                response.json().get("data", None)
            )
            category_container.usecase.insert(CategorySchema().dump(category))
            st.success(f"Category '{name}' created successfully!")
            load_category_data()
            st.session_state.dek = str(uuid.uuid4())  # Đổi khóa để làm mới bảng
            # Ẩn form sau khi submit
            st.session_state.show_form = False
        else:
            st.warning("Please upload an image or name!")

editor : pd.DataFrame = st.data_editor(
    st.session_state.df_category
    , column_config={
    "image_url": st.column_config.ImageColumn(
        "Preview Image",
        width=100,
        help="Image URL",
    ),
},
key=st.session_state.dek,
disabled=(["_id"]),
use_container_width=True,
hide_index=True)

c1,c2, c3= st.columns(3)
with c1:
    st.button("Reset", on_click=load_category_data, type='secondary', use_container_width=True)
with c2:
    st.button("Delete", on_click=delete_rows, use_container_width=True, type="secondary")
with c3:
    st.button("Save Changes", on_click=save_change, type='primary', use_container_width=True)
