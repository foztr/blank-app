import streamlit as st
import snowflake.connector

def app():
    st.title("Add Vendor")

    # Input form for vendor details
    with st.form("vendor_form"):
        vendor_name = st.text_input("Enter Vendor Name:")
        submitted = st.form_submit_button("Save Vendor")

        if submitted:
            if not vendor_name.strip():
                st.error("Vendor name cannot be empty!")
            else:
                try:
                    # Connect to Snowflake
                    my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
                    my_cur = my_cnx.cursor()

                    # Save the vendor to the database
                    my_cur.execute(f"INSERT INTO VENDORS (NAME) VALUES ('{vendor_name}')")
                    my_cnx.commit()

                    st.success(f"Vendor '{vendor_name}' saved successfully!")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
                finally:
                    my_cnx.close()
