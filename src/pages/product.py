import time
import uuid
import streamlit as st
import pandas as pd
import numpy as np
import os

from config import Config
from src.domain.schemas.image_schema import ImageSchema
from src.containers.category_container import CategoryContainer
from src.domain.schemas.product_schema import ProductSchema
from src.domain.schemas.image_schema import ImageSchema
from src.domain.entities.product import Product
from src.domain.entities.utils import get_new_uuid
from src.pages.container import repository_container
from src.containers.product_container import ProductContainer
from src.containers.image_container import ImageContainer
import requests
from streamlit_image_select import image_select

product_container = ProductContainer(repository_container)
category_container = CategoryContainer(repository_container)
image_container = ImageContainer(repository_container)
tab1, tab2= st.tabs(["Manage", "Create"])

category_datas = ProductSchema().dump(category_container.usecase.find_by_query({}), many=True)
formatted_options = [f"{category['name']}" for category in category_datas]

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
        else:
            st.session_state.df_product = pd.DataFrame()
        st.session_state.dek = str(uuid.uuid4())
    except Exception as e:
        st.session_state.df_product = pd.DataFrame()

if 'dek' not in st.session_state:
    st.session_state.dek = str(uuid.uuid4())
if "cate_id" not in st.session_state:
    st.session_state.cate_id = category_datas[0].get('_id')
if 'df_product' not in st.session_state:
    load_product_data()

def delete_rows():
    edited_df["Select"] = edited_df["Select"].fillna(False)
    selected_rows = edited_df[edited_df["Select"]]
    
    if selected_rows.empty:
        st.warning("No rows selected")
    else:
        for row in selected_rows.to_dict("records"):
            product_container.usecase.delete(row["_id"])  # Xóa trong DB
        st.success("Records deleted successfully.")
        load_product_data()

def upload_file(product_id, uploaded_files) -> str:
    files = [
        ("files", (file.name, file.getvalue(), file.type))
        for file in uploaded_files
    ]
    
    url = f"{Config.APP_HOST}/api/v1/images"  # URL của API upload file
    payload = {"product_id": _id, "feedback_id": ""}
    try:
        response = requests.post(url, files=files, data=payload)
        # Xử lý kết quả trả về từ API
        if response.status_code == 201:
            uploaded_urls = ImageSchema().load(response.json(), many=True)
            return uploaded_urls[0].get("url")
        else:
            return ""
    except Exception as e:
        return ""

@st.dialog(title="Update Product", width='large')
def update_product_dialog(product_dict):
    st.write("Update Product")
    st.write(product_dict)
    name = st.text_input("Product Name",value= product_dict["name"])
    des = st.text_area("Description",value= product_dict["description"])
    price = st.number_input("Price", value = product_dict["price"])
    quantity = st.number_input("Quantity", step=1, value = product_dict["quantity_sold"])
    total_time = st.number_input("Total time", step=1, value = product_dict["total_time"])
    
    data_dict = {item["_id"]: item["name"] for item in category_datas}

    name = data_dict.get(product_dict["category_id"], None)
    option = st.selectbox(
        "Category",
        options=formatted_options,
        index=formatted_options.index(name)
    )
    selected_index = formatted_options.index(option)
    selected_cate = category_datas[selected_index]
    cate_id = selected_cate["_id"]
    is_sold = st.checkbox("Is sold now", value=product_dict["is_sold"])
    product = Product(
        _id=product_dict["_id"],
        name=name,
        description=des,
        price=price,
        quantity_sold=quantity,
        is_sold=is_sold,
        total_time=total_time,
        category_id=cate_id,
        thumbnail=product_dict["thumbnail"],
        discount_id=None,
        feedback_id=None
    )
    with st.form("form_image", clear_on_submit=True):
        image_datas = ImageSchema().dump(image_container.usecase.find_by_query({"product_id": product_dict["_id"]}), many=True)
        list_image = [image['url'] for image in image_datas]
        uploaded_files = st.file_uploader("Add Image", accept_multiple_files=True, type=(["png", "jpg", "webp", "gif"]))
        if st.form_submit_button("Add", type='primary'):
            print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>" + upload_file(product._id, uploaded_files))
        if len(image_datas) > 0:
            img = image_select(
                label="Manage Image Of Product",
                images=list_image,
                use_container_width=True
            )
            img_selected = {item["url"] : item['_id'] for item in image_datas}
            print(img_selected)
            img_id = img_selected.get(img, None)
            print(img_id)
        c1, c2 = st.columns(2)
        with c1:
            if st.form_submit_button("Delete", type='secondary'):
                image_container.usecase.delete(img_id)
        with c2:
            if st.form_submit_button(label="Save", type="primary"):
                product.thumbnail = img_id
                st.write(uploaded_files)
    if st.button("Update Product", type="primary", use_container_width=True):
        product_container.usecase.update(product._id, ProductSchema().dump(product))
        st.rerun()

with tab2:
    tab2.subheader("Create New Product")
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
                product.thumbnail = upload_file(_id, uploaded_files)
            product_container.usecase.insert(ProductSchema().dump(product))
            banner = st.success("Create Product Successfully!")
            time.sleep(3)
            banner.empty()




with tab1:
    st.write("## Sort by Category")
    option = st.selectbox(
        "Select Category of product you want to see.",
        options=formatted_options
    )
    selected_index = formatted_options.index(option)
    selected_cate = category_datas[selected_index]
    cate_id = selected_cate["_id"]
    if 'cate_id' not in st.session_state or st.session_state['cate_id'] != cate_id:
        st.session_state.cate_id = cate_id
        load_product_data()

    # load_product_data()
    st.write("## List Product")
    edited_df = st.data_editor(
        st.session_state.df_product,
        num_rows="dynamic",
        use_container_width=True,
        disabled=["_id"],
        column_config={
            "thumbnail": st.column_config.ImageColumn(
                "Preview Image",
                width=100,
            ),
        },
        key=st.session_state.dek,
    )

    c1,c2, c3 = st.columns(3)
    with c1:
        st.button("Reset", on_click=load_product_data, type='secondary', use_container_width=True)
    with c2:
        st.button("Delete", on_click=delete_rows, use_container_width=True, type="primary")
    with c3:
        if st.button("Update", use_container_width=True):
            edited_df["Select"] = edited_df["Select"].fillna(False)
            selected_rows = edited_df[edited_df["Select"]]
            
            if selected_rows.empty:
                st.warning("No rows selected")
            elif len(selected_rows) != 1:
                st.warning("Please select one row you want to update")
            else:
                update_product_dialog(selected_rows.to_dict("records")[0])