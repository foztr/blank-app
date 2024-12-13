import streamlit as st
import snowflake.connector

def app():
    st.title("Add Product")

    # Input form for product details
    with st.form("product_form"):
        product_name = st.text_input("Enter Product Name:")
        submitted = st.form_submit_button("Save Product")

        if submitted:
            if not product_name.strip():
                st.error("Product name cannot be empty!")
            else:
                try:
                    # Connect to Snowflake
                    my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
                    my_cur = my_cnx.cursor()

                    # Save the product to the database
                    my_cur.execute(f"INSERT INTO PRODUCTS (NAME) VALUES ('{product_name}')")
                    my_cnx.commit()

                    st.success(f"Product '{product_name}' saved successfully!")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
                finally:
                    my_cnx.close()
