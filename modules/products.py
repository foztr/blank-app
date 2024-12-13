import streamlit as st
import snowflake.connector
import pandas as pd

# Function to fetch products from Snowflake with pagination
def get_products_from_db(page_num=1, page_size=10):
    """Fetch a subset of products from the Snowflake database with pagination."""
    # Connect to Snowflake
    my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
    my_cur = my_cnx.cursor()

    # Define SQL query with LIMIT and OFFSET for pagination
    offset = (page_num - 1) * page_size
    query = f"SELECT id, name FROM PRODUCTS LIMIT {page_size} OFFSET {offset}"

    # Execute the query and fetch the results
    my_cur.execute(query)
    products = my_cur.fetchall()

    # Optionally, create a pandas DataFrame for easy manipulation
    df = pd.DataFrame(products, columns=["ID", "Name"])

    # Close the connection
    my_cur.close()
    my_cnx.close()

    return df

# Main page to list products
def app():
    # Display Products Page Title
    st.title("Products")

    # Define page size for pagination
    page_size = 10

    # Assuming you know the total number of products in your table, for example, 100
    total_products = 100  # Replace with actual total number from the database
    total_pages = (total_products // page_size) + (1 if total_products % page_size > 0 else 0)

    # Initialize session state for page number if not set
    if 'page_num' not in st.session_state:
        st.session_state.page_num = 1

    page_num = st.session_state.page_num

    # Fetch the products for the current page
    products_df = get_products_from_db(page_num, page_size)

    # Drop the ID column to hide it
    products_df = products_df.drop(columns=["ID"])

    # Display the products in a full-width table
    st.dataframe(products_df, use_container_width=True)

    # Pagination controls: Previous and Next buttons with current page display
    st.markdown("---")  # Adds a horizontal line for better layout separation
    col1, col2, col3 = st.columns([1, 2, 1])  # Adjust column proportions for better layout

    with col1:
        # Display Previous button only if not on the first page
        if page_num > 1:
            if st.button("Previous"):
                st.session_state.page_num -= 1
                st.rerun()

    with col2:
        # Display current page number out of total pages
        st.markdown(f"**Page {page_num} of {total_pages}**", unsafe_allow_html=True)

    with col3:
        # Display Next button only if not on the last page
        if page_num < total_pages:
            if st.button("Next"):
                st.session_state.page_num += 1
                st.rerun()

    # Optional: Show feedback if there are no products
    if products_df.empty:
        st.write("No products available.")

    
 