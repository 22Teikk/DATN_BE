import streamlit as st

def create_form_from_object(obj):
    form_data = {}
    for attr in dir(obj):  # Lấy tất cả các thuộc tính và phương thức của đối tượng
        if not attr.startswith("__"):  # Bỏ qua các phương thức nội bộ của Python
            attr_value = getattr(obj, attr)  # Lấy giá trị của thuộc tính
            # Tạo các widget dựa trên kiểu của thuộc tính
            if isinstance(attr_value, str):
                form_data[attr] = st.text_input(attr, attr_value)
            elif isinstance(attr_value, int):
                form_data[attr] = st.number_input(attr, value=attr_value)
            elif isinstance(attr_value, bool):
                form_data[attr] = st.checkbox(attr, value=attr_value)
    
    return form_data