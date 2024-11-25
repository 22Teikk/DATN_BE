import streamlit as st
from st_pages import add_page_title, get_nav_from_toml
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

with open(".streamlit/auth.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    "",
    "1234567890",
    30,
)

name, authentication_status, user = authenticator.login(location="sidebar")

def init_pages():
    nav = get_nav_from_toml(".streamlit/pages.toml")
    st.logo("https://app-service.hihoay.io/files/ic_hihoay.png")
    pg = st.navigation(nav)
    add_page_title(pg)
    pg.run()
    st.write("---")


if authentication_status:
    authenticator.logout(location="sidebar")
    st.sidebar.write(f'Welcome `{name}`!')
    init_pages()
elif authentication_status is False:
    st.sidebar.error("Username/password is incorrect")
elif authentication_status is None:
    st.sidebar.warning("Please enter your username and password")