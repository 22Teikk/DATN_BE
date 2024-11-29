import uuid
import streamlit as st
import pandas as pd
import numpy as np
import os

from src.domain.schemas.store_schema import StoreSchema
from src.domain.entities.store import Store
from src.domain.entities.utils import get_new_uuid
from src.pages.utils import create_form_from_object
from src.pages.container import repository_container
from src.containers.store_container import StoreContainer

store_container = StoreContainer(repository_container)
store = store_container.usecase.find_by_id("77c611bd-9195-4d54-a48c-a526e16c31df")

def update_store(store):
    store_container.usecase.update(StoreSchema().dump(store))

st.write("## Store")
st.image(store['image_src'])
name = st.text_input(label="Store name",value=store['name'])
address = st.text_input(label="Address",value=store['address'])
des = st.text_input(label="Description",value=store['description'])
open_time = st.text_input(label="Open time",value=store['open_time'])
close_time = st.text_input(label="Close time",value=store['close_time'])
open_day = st.text_input(label="Open day",value=store['open_day'])
phone = st.text_input(label="Phone number",value=store['phone'])
email = st.text_input(label="Email address",value=store['email'])
store_model = Store(
    _id = "77c611bd-9195-4d54-a48c-a526e16c31df",
    name = name,
    address = address,
    description = des,
    lat = store['lat'],
    long = store['long'],
    open_time = open_time,
    close_time = close_time,
    open_day = open_day,
    phone = phone,
    email = email,
    image_src = store['image_src']
)
if st.button("Update", type='primary', use_container_width=True):
    update_store(store_model)
    st.success("Store updated successfully!")
    st.rerun()