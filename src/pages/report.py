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

category_data = CategorySchema().dump(category_container.usecase.find_by_query(), many=True)
products_data = ProductSchema().dump(product_container.usecase.find_by_query(), many=True)
orders_data = OrderSchema().dump(order_container.usecase.find_by_query(), many=True)
order_items_data = OrderItemSchema().dump(order_item_container.usecase.find_by_query(), many=True)

def load_revenue_report():
    # Giả sử bạn đã có dữ liệu từ các bảng Order và OrderItem
    orders_df = pd.DataFrame(orders_data)  # orders_data là danh sách dict từ bảng Order
    order_items_df = pd.DataFrame(order_items_data)  # order_items_data là danh sách dict từ bảng OrderItem

    # Bước 1: Chuyển đổi cột created_at thành kiểu datetime
    orders_df["created_at"] = pd.to_datetime(orders_df["created_at"], format="%Y-%m-%d %H:%M:%S")

    # Bước 2: Merge dữ liệu giữa Order và OrderItem để tính doanh thu
    revenue_data = pd.merge(order_items_df, orders_df, left_on="order_id", right_on="_id", how="inner")

    # Bước 3: Tính doanh thu cho mỗi OrderItem
    revenue_data["revenue"] = revenue_data["quantity"] * revenue_data["price"]

    # Bước 4: Tạo các cột thời gian theo ngày, tháng, và năm
    revenue_data["day"] = revenue_data["created_at"].dt.date
    revenue_data["month"] = revenue_data["created_at"].dt.to_period("M").dt.to_timestamp()
    revenue_data["year"] = revenue_data["created_at"].dt.to_period("Y").dt.to_timestamp()

    # Bước 5: Tính tổng doanh thu theo ngày
    daily_revenue = revenue_data.groupby("day").agg(total_revenue=("revenue", "sum")).reset_index()

    # Bước 6: Tính tổng doanh thu theo tháng
    monthly_revenue = revenue_data.groupby("month").agg(total_revenue=("revenue", "sum")).reset_index()

    # Bước 7: Tính tổng doanh thu theo năm
    yearly_revenue = revenue_data.groupby("year").agg(total_revenue=("revenue", "sum")).reset_index()

    col1, col2, col3 = st.columns(3)
    # Bước 8: Hiển thị kết quả
    with col1:
        st.write("#### Total Revenue")
        st.write(f"${daily_revenue['total_revenue'].sum():,.2f}")

    with col2:
        st.write("#### Average Revenue per Month")
        st.write(f"${monthly_revenue['total_revenue'].mean():,.2f}")

    with col3:
        st.write("#### Average Revenue per Month")
        st.write(f"${yearly_revenue['total_revenue'].mean():,.2f}")

def load_order_count_report():
    # Giả sử bạn đã có dữ liệu từ bảng Order
    orders_df = pd.DataFrame(orders_data)  # orders_data là danh sách dict từ bảng Order

    # Bước 1: Chuyển đổi cột created_at thành kiểu datetime
    orders_df["created_at"] = pd.to_datetime(orders_df["created_at"], format="%Y-%m-%d %H:%M:%S")

    # Bước 2: Lấy ngày, tháng, và năm hiện tại
    today = datetime.now().date()
    current_month = today.replace(day=1).strftime("%Y-%m")
    current_year = today.replace(month=1, day=1).strftime("%Y")

    # Bước 3: Tạo các cột thời gian theo ngày, tháng, năm
    orders_df["day"] = orders_df["created_at"].dt.date
    orders_df["month"] = orders_df["created_at"].dt.to_period("M")
    orders_df["year"] = orders_df["created_at"].dt.to_period("Y")
    # Bước 4: Lọc đơn hàng theo ngày hiện tại
    daily_order_count = orders_df[orders_df["day"] == today].shape[0]

    
    # Bước 5: Lọc đơn hàng theo tháng hiện tại
    monthly_order_count = orders_df[orders_df["month"] == current_month].shape[0]

    # Bước 6: Lọc đơn hàng theo năm hiện tại
    yearly_order_count = orders_df[orders_df["year"] == current_year].shape[0]


    # Bước 7: Hiển thị kết quả
    col1, col2, col3 = st.columns(3)    
    with col1:
        st.write(f"### Total Orders Today")
        st.write(str(daily_order_count))
    with col2:
        st.write(f"### Total Orders This Month")
        st.write(str(monthly_order_count))
    with col3:    
        st.write(f"### Total Orders This Year")
        st.write(str(yearly_order_count))
    st.write("## Order Table")
    st.write(orders_df)


load_revenue_report()
load_order_count_report()