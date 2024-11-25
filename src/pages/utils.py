import streamlit as st
from marshmallow import fields, Schema

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

def schema_to_form(schema_class, form_key="default_form", submit_label="Submit", special_fields=None):
    """
    Tạo form từ schema với Streamlit, hỗ trợ trường đặc biệt như file upload.

    Args:
        schema_class (Schema): Lớp schema từ Marshmallow.
        form_key (str): Khóa duy nhất cho form.
        submit_label (str): Nhãn cho nút submit.
        special_fields (dict): Từ điển chứa các trường đặc biệt cần xử lý (ví dụ: {"thumbnail": "file_upload"}).

    Returns:
        dict: Giá trị được nhập trong form.
    """
    schema_fields = schema_class().fields
    field_values = {}

    if special_fields is None:
        special_fields = {}

    with st.form(form_key):
        for field_name, field in schema_fields.items():
            label = field.metadata.get("description", field_name)  # Lấy mô tả nếu có, nếu không dùng tên trường
            default_value = field.default if field.default is not None else None

            # Kiểm tra nếu trường cần xử lý đặc biệt
            if field_name in special_fields and special_fields[field_name] == "file_upload":
                file = st.file_uploader(label, type=["png", "jpg", "jpeg"], key=f"{form_key}_{field_name}")
                if file is not None:
                    # Chuyển file thành URL hoặc base64 string
                    field_values[field_name] = {
                        "filename": file.name,
                        "content": file.getvalue()
                    }  # Lưu cả tên file và nội dung file
                else:
                    field_values[field_name] = None

            # Xử lý các kiểu trường thông thường
            elif isinstance(field, fields.Str):
                field_values[field_name] = st.text_input(label, value=default_value or "", placeholder=f"Enter {label}")
            elif isinstance(field, fields.Float):
                field_values[field_name] = st.number_input(label, value=default_value or 0.0, step=0.01, format="%.2f")
            elif isinstance(field, fields.Int):
                field_values[field_name] = st.number_input(label, value=default_value or 0, step=1)
            elif isinstance(field, fields.Bool):
                field_values[field_name] = st.checkbox(label, value=default_value or False)
            elif isinstance(field, fields.Date):
                field_values[field_name] = st.date_input(label)
            elif isinstance(field, fields.DateTime):
                field_values[field_name] = st.text_input(label, value="", placeholder="Enter datetime (YYYY-MM-DD HH:MM:SS)")
            elif isinstance(field, fields.Url):
                field_values[field_name] = st.text_input(label, value=default_value or "", placeholder=f"Enter {label} (URL format)")
            elif isinstance(field, fields.List):
                st.warning(f"Field '{label}' is a list. Please implement a custom handler.")
            else:
                st.warning(f"Field type for '{label}' not supported yet!")

        # Nút submit
        submitted = st.form_submit_button(submit_label)
        if submitted:
            # Xử lý giá trị mặc định cho các trường không bắt buộc
            for field_name, field in schema_fields.items():
                if not field.required and field_name not in field_values:
                    field_values[field_name] = None
            return field_values

    return None
