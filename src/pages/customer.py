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

@st.cache_data(ttl=60)
def load_data():
    st.session_state.orders_data = OrderSchema().dump(order_container.usecase.find_by_query(), many=True)
    st.session_state.order_items_data = OrderItemSchema().dump(order_item_container.usecase.find_by_query(), many=True)
    st.session_state.users_data = UserProfileSchema().dump(user_container.usecase.find_by_query({"role_id": "1"}), many=True)
def load_user_data():
    data = user_container.usecase.find_by_query({"role_id": "1"})
    df = pd.DataFrame.from_dict(data)
    
    if not df.empty:
        if "Select" not in df.columns:
            df.insert(0, "Select", False) 
        else:
            select_col = df.pop("Select")
            df.insert(0, "Select", False) 
        
    st.session_state.df_app = df
    st.session_state.dek = str(uuid.uuid4()) 
    load_data()

if 'dek' not in st.session_state:
    st.session_state.dek = str(uuid.uuid4())
if 'df_app' not in st.session_state:
    load_user_data()

def delete_rows():
    edited_df["Select"] = edited_df["Select"].fillna(False)
    selected_rows = edited_df[edited_df["Select"]]
    if selected_rows.empty:
        st.warning("No rows selected")
    else:
        for row in selected_rows.to_dict("records"):
            user_container.usecase.delete(row["_id"]) 
        load_user_data()

def save_records():
    records = edited_df.drop(columns=["Select"]).to_dict("records")  # Bỏ cột Select
    for record in records:
        if "_id" not in record or not record["_id"] or np.isnan(record["_id"]):
            record["_id"] = get_new_uuid()  # Tự sinh `_id` nếu chưa có
    user_container.usecase.upserts(records)  # Lưu dữ liệu vào DB


import plotly.figure_factory as ff
import plotly.express as px

col1, col2 = st.columns(2)

def load_user_order_most():
    users_df = pd.DataFrame(st.session_state.users_data)
    orders_df = pd.DataFrame(st.session_state.orders_data)

    merged_df = orders_df.merge(users_df, left_on="user_id", right_on="_id", how="inner")

    order_count = merged_df.groupby(["user_id", "name"])["_id_x"].count().reset_index()

    order_count.rename(columns={"_id_x": "order_count"}, inplace=True)

    order_count = order_count.sort_values(by="order_count", ascending=False)
    
    st.write("## Users with the Most Orders")
    st.write(order_count)

def load_user_order_cost():
    users_df = pd.DataFrame(st.session_state.users_data)
    orders_df = pd.DataFrame(st.session_state.orders_data)
    order_items_df = pd.DataFrame(st.session_state.order_items_data)

    order_items_with_user = order_items_df.merge(orders_df, left_on="order_id", right_on="_id", how="inner")

    order_items_with_user = order_items_with_user.merge(users_df, left_on="user_id", right_on="_id", how="inner")

    order_items_with_user["total_price"] = order_items_with_user["quantity"] * order_items_with_user["price"]

    user_total_spending = order_items_with_user.groupby(["user_id", "name"])["total_price"].sum().reset_index()

    user_total_spending.rename(columns={"total_price": "total_spent"}, inplace=True)

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

c1, c2, c3 = st.columns(3)

with c1:
    st.button("Reset", on_click=load_user_data ,use_container_width=True, type="secondary")

with c2:
    st.button("Delete", on_click=delete_rows, use_container_width=True, type="secondary")

with c3:
    st.button("Save Change", on_click=save_records, use_container_width=True, type="primary")


load_user_order_most()
load_user_order_cost()
