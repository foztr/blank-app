import streamlit as st
from streamlit_option_menu import option_menu
from modules import home,  products, addProduct, vendors, addVendor
import snowflake.connector




# Sidebar for navigation
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "Products", "Add Product", "Vendors", "Add Vendor"],  # Add "Products"
        icons=["house", "list", "list", "list", "list"],
        menu_icon="cast",
        default_index=0,
    )


# Render the selected page
if selected == "Home":
    home.app()
elif selected == "Products":
    products.app()  # List products page
elif selected == "Add Product":
    addProduct.app()  # Add products page
elif selected == "Vendors":
    vendors.app()  # List vendors page
elif selected == "Add Vendor":
    addVendor.app()  # Add vendors page