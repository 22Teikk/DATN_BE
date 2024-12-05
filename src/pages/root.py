from datetime import datetime
import uuid
import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.express as px


from src.domain.entities.utils import get_new_uuid
from src.pages.container import repository_container

from src.containers.order_item_container import OrderItemContainer
from src.containers.order_container import OrderContainer
from src.containers.category_container import CategoryContainer
from src.containers.product_container import ProductContainer

from src.domain.schemas.order_schema import OrderSchema 
from src.domain.schemas.category_schema import CategorySchema 
from src.domain.schemas.product_schema import ProductSchema 
from src.domain.schemas.order_item_schema import OrderItemSchema 

order_container = OrderContainer(repository_container)
order_item_container = OrderItemContainer(repository_container)
product_container = ProductContainer(repository_container)
category_container = CategoryContainer(repository_container)

@st.cache_data(ttl=60)
def load_data():
    st.session_state.category_data = CategorySchema().dump(category_container.usecase.find_by_query(), many=True)
    st.session_state.products_data = ProductSchema().dump(product_container.usecase.find_by_query(), many=True)
    st.session_state.orders_data = OrderSchema().dump(order_container.usecase.find_by_query(), many=True)
    st.session_state.order_items_data = OrderItemSchema().dump(order_item_container.usecase.find_by_query(), many=True)

if 'category_data' or 'products_data' or 'orders_data' or 'order_items_data' not in st.session_state:
    load_data()

def load_pie_chart_product_sale():
    order_items_df = pd.DataFrame(st.session_state.order_items_data)
# Tính tổng số lượng cho mỗi sản phẩm
    product_sales = order_items_df.groupby("product_id")["quantity"].sum().reset_index()

    # Bước 2: Lấy tên sản phẩm từ list products
    # Tạo một dictionary từ list products để tra cứu tên sản phẩm
    product_names = {product["_id"]: product["name"] for product in st.session_state.products_data}

    # # Thêm cột "product_name" vào product_sales
    product_sales["product_name"] = product_sales["product_id"].map(product_names)

    # # Bước 3: Vẽ Pie chart
    return px.pie(product_sales, 
            names='product_name', 
            values='quantity', 
            title="Product Order Distribution", 
            hole=0.3)  # Chế độ donut nếu muốn

# Hiển thị Pie chart trong Streamlit
    

def chart_product_sale_by_category():
    orders_df = pd.DataFrame(st.session_state.orders_data)
    order_items_df = pd.DataFrame(st.session_state.order_items_data)
    products_df = pd.DataFrame(st.session_state.products_data)
    categories_df = pd.DataFrame(st.session_state.category_data)
    # Bước 1: Kết hợp OrderItem và Product để tính số lượng bán được của từng sản phẩm
    merged_df = pd.merge(order_items_df, products_df, left_on="product_id", right_on="_id", how="inner")

# Bước 2: Tính tổng số lượng bán được của từng sản phẩm
    sales_by_product = merged_df.groupby(['category_id', 'name'])['quantity'].sum().reset_index()

    col1, col2 = st.columns(2)
    with col1:
        status_count = orders_df['status'].value_counts().reset_index()
        status_count.columns = ['status', 'count']

        # Tạo Pie chart cho tỷ lệ đơn hàng theo status
        status_fig = px.pie(status_count,
                            names='status',
                            values='count',
                            title='Order Status Distribution',
                            hole=0.3)  # Chế độ donut

        # Hiển thị Pie chart của order status
        st.plotly_chart(status_fig)
    with col2:
        st.plotly_chart(load_pie_chart_product_sale())

# Bước 4: Vẽ Pie chart cho từng Category và hiển thị trên các cột
    for i, category in categories_df.iterrows():
        category_id = category["_id"]
        category_name = category["name"]
        
        # Lọc các sản phẩm trong danh mục
        category_sales = sales_by_product[sales_by_product['category_id'] == category_id]
        
        # Tạo Pie chart
        fig = px.pie(category_sales,
                    names="name",
                    values="quantity",
                    title=f"Sales Distribution for {category_name}",
                    hole=0.3)  # Chế độ donut
        
        # Chia cột để vẽ các Pie chart
        if i % 2 == 0:
            col1.plotly_chart(fig)  # Đặt chart vào cột 1
        else:
            col2.plotly_chart(fig) 
    

st.write("## Statistical")
chart_product_sale_by_category()