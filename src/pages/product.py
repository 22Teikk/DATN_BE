import uuid
import streamlit as st
import pandas as pd
import numpy as np
import os

from src.domain.schemas.image_schema import ImageSchema
from src.containers.category_container import CategoryContainer
from src.domain.schemas.product_schema import ProductSchema
from src.domain.entities.product import Product
from src.domain.entities.utils import get_new_uuid
from src.pages.utils import create_form_from_object, schema_to_form
from src.pages.container import repository_container
from src.containers.product_container import ProductContainer
import requests

product_container = ProductContainer(repository_container)
category_container = CategoryContainer(repository_container)
tab1, tab2 = st.tabs(["Create", "Manage"])

def load_product_data():
    try:
        if st.session_state.cate_id:
            products = ProductSchema().dump(product_container.usecase.find_by_query({"category_id" : st.session_state.cate_id}), many=True)
        else :
            products = ProductSchema().dump(product_container.usecase.find_by_query(), many=True)
        df = pd.DataFrame.from_dict(products)
        if not df.empty:
            # Kiểm tra nếu cột 'Select' chưa tồn tại, nếu chưa thì thêm vào
            if "Select" not in df.columns:
                df.insert(0, "Select", False)  # Thêm cột checkbox vào vị trí đầu tiên
            else:
                # Nếu cột 'Select' đã tồn tại nhưng không ở đầu, đưa nó về đầu
                select_col = df.pop("Select")
                df.insert(0, "Select", False)  # Đảm bảo cột 'Select' ở vị trí đầu tiên

            st.session_state.df_product = df
    except Exception as e:
        st.session_state.df_product = None

category_datas = ProductSchema().dump(category_container.usecase.find_by_query({}), many=True)
formatted_options = [f"{category['name']}" for category in category_datas]

if 'dek' not in st.session_state:
    st.session_state.dek = str(uuid.uuid4())
if "cate_id" not in st.session_state:
    st.session_state.cate_id = None
if 'df_product' not in st.session_state:
    st.session_state.df_product = None

with tab1:
    tab1.subheader("Create New Product")
    with st.form("form_product", clear_on_submit=True):
        _id = get_new_uuid()
        name = st.text_input("Product Name")
        des = st.text_area("Description")
        price = st.number_input("Price")
        quantity = st.number_input("Quantity", step=1)
        total_time = st.number_input("Total time", step=1)
        option = st.selectbox(
            "Category",
            options=formatted_options
        )
        selected_index = formatted_options.index(option)
        selected_cate = category_datas[selected_index]
        cate_id = selected_cate["_id"]
        is_sold = st.checkbox("Is sold now", value=True)
        product = Product(
            _id=_id,
            name=name,
            description=des,
            price=price,
            quantity_sold=quantity,
            is_sold=is_sold,
            total_time=total_time,
            category_id=cate_id,
            thumbnail="",
            discount_id=None,
            feedback_id=None
        )
        uploaded_files = st.file_uploader("Selected Image", accept_multiple_files=True, type=(["png", "jpg", "webp", "gif"]))
        if st.form_submit_button("Create", type='primary', use_container_width=True):
            if uploaded_files:
                files = [
                    ("files", (file.name, file.getvalue(), file.type))
                    for file in uploaded_files
                ]
                
                url = f"{os.getenv('APP_HOST')}/api/v1/images"  # URL của API upload file
                payload = {"product_id": _id, "feedback_id": ""}
                try:
                    response = requests.post(url, files=files, data=payload)
                    
                    # Xử lý kết quả trả về từ API
                    if response.status_code == 201:
                        uploaded_urls = ImageSchema().load(response.json(), many=True)
                        product.thumbnail = uploaded_urls[0].get("url")
                    else:
                        st.error(f"Failed to upload files: {response.text}")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
            product_container.usecase.insert(ProductSchema().dump(product))
            st.success("Create Product Successfully!")


with tab2:
    st.write("## Sort by Category")
    option = st.selectbox(
        "Select Category of product you want to see.",
        options=formatted_options
    )
    selected_index = formatted_options.index(option)
    selected_cate = category_datas[selected_index]
    st.write(selected_cate)
    cate_id = selected_cate["_id"]

    st.write("## List Product")
    edited_df = st.data_editor(
        st.session_state.df_product,
        num_rows="dynamic",
        use_container_width=True,
        disabled=["_id"],
        key=st.session_state.dek,
        column_config={
            "category_id": st.column_config.SelectboxColumn(
                "Category",
                width="medium",
                options=formatted_options,
            )
        }
    )

    c1,c2, c3 = st.columns(3)
    with c1:
        if st.button("Reset", type='secondary', use_container_width=True):
            load_product_data()
            st.session_state.dek = str(uuid.uuid4())  # Đổi khóa để làm mới bảng
    with c3:
        if st.button("Delete", use_container_width=True, type="primary"):
            edited_df["Select"] = edited_df["Select"].fillna(False)
            
            # Lọc các dòng được chọn
            selected_rows = edited_df[edited_df["Select"]]
            
            if selected_rows.empty:
                st.warning("No rows selected")
            else:
                for row in selected_rows.to_dict("records"):
                    category_container.usecase.delete(row["_id"])  # Xóa trong DB
                st.success("Records deleted successfully.")
                load_product_data()
                st.session_state.dek = str(uuid.uuid4())  # Đổi khóa để làm mới bảng   
    with c2:
        if st.button("Update", use_container_width=True, type="secondary"):
            edited_df["Select"] = edited_df["Select"].fillna(False)
            
            # Lọc các dòng được chọn
            selected_rows = edited_df[edited_df["Select"]]
            
            if selected_rows.empty:
                st.warning("No rows selected")
            elif len(selected_rows) != 1:
                st.warning("Please selected one row to update!")
            else:
                st.write("Update")


