import streamlit as st
import pandas as pd
from pymongo import MongoClient
import plotly.express as px
from bson.objectid import ObjectId
# MongoDB setup
mongo_uri = "mongodb+srv://gauravmcanada:Gaurav9839@cluster0.0hb6u6c.mongodb.net/"  # Replace with your MongoDB Atlas connection string
client = MongoClient(mongo_uri)
db = client['scrapy']  # Your database name
# Function to process collection data

def process_collection_data(collection):
    df = pd.DataFrame(list(collection.find()))
    df['price'] = df['price'].replace('[\£]', '', regex=True).astype(float)
    avg_price = df['price'].mean()
    num_ids = len(df)
    in_stock_count = df['inStock'].sum()
    return df, avg_price, num_ids, in_stock_count

# Streamlit app
st.title(' Book Spectrum')



# Custom CSS for sidebar using inline styles
sidebar_style = """
<style>
div[data-testid="stSidebar"] .css-1d391kg {
    background-color: #1E2A39;  /* Dark Blue */
}
div[data-testid="stSidebar"] .css-1d391kg .css-1v3fvcr {
    font-weight: bold;
    color: white;
    text-align: center;
    padding: 5px;
    font-size: 20px; /* Adjust size as needed */
    margin: 0;
}
</style>
"""

# Injecting the custom style into the Streamlit interface
st.markdown(sidebar_style, unsafe_allow_html=True)

# Sidebar content with sections
st.sidebar.title("Group Members")
st.sidebar.markdown("""
- Rupal Bhatia
- Gaurav Mehta
- Pooja Yadav
""")

st.sidebar.title("Solution Architecture")
st.sidebar.markdown("""
- **Web scraper Tool:** Scrapy
- **Website scraped:** [books.toscrape.com](https://books.toscrape.com/catalogue/category/books_1/index.html)
- **Sections scraped:** Book
- **Genres scraped:** 5
- **Database to store:** MongoDB Atlas
- **Database link:** [MongoDB Cloud](https://cloud.mongodb.com/v2/6574196ec040b63e707000b4#/metrics/replicaSet/657419da782bf66ce0c73c03/explorer/scrapy/classics_6/find)
- **Python tool for frontend:** Streamlit
- **API for PUSH and GET DB:** Pymongo
""", unsafe_allow_html=True)


# Display collections in a card layout
collection_data = {}
collection_names = db.list_collection_names()

# Display collections in a card layout
collection_data = {}
collection_names = db.list_collection_names()

# Define columns for the grid layout
grid_cols = 5
st.markdown('<p style="text-align: center; color: darkgrey; font-weight: bold;">Genre of Books scraped with KPI</p>', unsafe_allow_html=True)

# Streamlit columns are created dynamically based on the number of collections
for index, name in enumerate(collection_names):
    if index % grid_cols == 0:
        cols = st.columns(grid_cols)
    
    collection = db[name]
    
    df, avg_price, num_ids, in_stock_count = process_collection_data(collection)
    collection_data[name] = df
    
    # Calculate which column this card should be in
    display_name = name.split('_')[0].split('-')[0]
    col_index = index % grid_cols
    
    # Define the card style with inline CSS
    card_style = """
    <div style="
        border: 2px solid #1E2A39;  /* Dark blue border */
        background-color: #000000;  /* Black background */
        color: #FFFFFF;             /* White text */
        text-align: center;         /* Centered text */
        padding: 16px;
        border-radius: 10px;
        margin: 10px 0;
    ">
        <h4 style='margin-left:2px ;'><strong>{collection_name}</strong></h4>
        <p style='margin-bottom:0.5rem;'><strong>Avg Price:</strong> £{avg_price:.2f}</p>
        <p style='margin-bottom:0.5rem;'><strong>Total IDs:</strong> {num_ids}</p>
        <p style='margin-bottom:0.5rem;'><strong>In Stock:</strong> {in_stock_count}</p>
    </div>
    """
    
    # Display the collection data as a card in the appropriate column
    with cols[col_index]:
        st.markdown(card_style.format(collection_name=display_name, avg_price=avg_price, num_ids=num_ids, in_stock_count=in_stock_count), unsafe_allow_html=True)
# Interactivity on selecting a collection

st.markdown("<hr>", unsafe_allow_html=True)  # Horizontal line
st.markdown('<h2 style="text-align: center; color:darkblue;"> Genre Analysis </h2>', unsafe_allow_html=True) 


# Create a layout with two columns
col1, col2 = st.columns([3, 1])  # Adjust the ratio as needed

with col1:
    selected_collection = st.selectbox("Select a collection to view details:", list(collection_data.keys()))

with col2:
    if selected_collection:
        st.write(f"Selected: {selected_collection}")
    else:
        st.write("No collection selected")
        
        
#selected_collection = st.selectbox("Select a collection to view details:", list(collection_data.keys()))
if selected_collection:
    df = collection_data[selected_collection]
    st.dataframe(df[['title', 'rating', 'price', 'inStock']],use_container_width=True)
    
    
        # Convert ratings to numeric
    rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    df['rating_numeric'] = df['rating'].map(rating_map)
      # Collapsible section for detailed analysis
    with st.expander("Detailed Analysis of the Selected Genre:{selected_collection}"):
        # Count of ID and titles
        count_of_ids = len(df)
        count_of_titles = df['title'].nunique()
        st.markdown(f"<p style='text-align: center; font-weight: bold; font-size: 20px;'>Count of IDs: {count_of_ids}</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; font-weight: bold; font-size: 20px;'>Count of unique titles: {count_of_titles}</p>", unsafe_allow_html=True)
        # Number of IDs by rating
        ids_by_rating = df['rating'].value_counts()
        
        st.write("Number of IDs by rating:")
        st.write(ids_by_rating)

        # Average price per rating
        avg_price_per_rating = df.groupby('rating')['price'].mean()
        st.write("Average price per rating:")
        st.write(avg_price_per_rating)

        # Top 5 rated IDs and their prices and titles
        top_rated = df.nlargest(5, 'rating_numeric')
        st.write("Top 5 rated IDs based on numeric rating:")
        st.write(top_rated[['title', 'price', 'rating']])
    
    
    
    st.markdown("<hr>", unsafe_allow_html=True)  # Horizontal line
    st.markdown('<h2 style="text-align: center; color:darkblue;"> By Title Filtering  </h2>', unsafe_allow_html=True) 

    
     # Title filter
    title_filter = st.text_input("Filter by title on the above selected genre:")
    
    if title_filter:
        # Filter the DataFrame based on the title
        filtered_df_title = df[df['title'].str.contains(title_filter, case=False, na=False)]
        st.subheader(f"Items matching title '{title_filter}' in {selected_collection}")
        st.dataframe(filtered_df_title,use_container_width=True)
    else:
        # If the title filter is empty, display all rows
        st.subheader(f"All items in {selected_collection}")
        st.dataframe(df,use_container_width=True)
        
        
    st.markdown("<hr>", unsafe_allow_html=True)  # Horizontal line
    st.markdown('<h2 style="text-align: center; color:darkblue;">Filter by Rating and Price</h2>', unsafe_allow_html=True)

    # Columns for sliders
    col1, col2 = st.columns(2)

    # Rating slider
    with col1:
        min_rating, max_rating = st.slider("Filter by rating range:", 1, 5, (1, 5))

    # Price slider
    with col2:
        min_price, max_price = st.slider("Filter by price range (£):", float(df['price'].min()), float(df['price'].max()), (float(df['price'].min()), float(df['price'].max())))

    # Map textual ratings to numeric if needed
    rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    if 'rating' in df.columns and df['rating'].dtype == 'object':
        df['rating_numeric'] = df['rating'].map(rating_map)
    else:
        df['rating_numeric'] = df['rating']  # Assuming rating is already numeric

    # Filter the DataFrame based on sliders
    filtered_df = df[(df['rating_numeric'] >= min_rating) & (df['rating_numeric'] <= max_rating) & (df['price'].between(min_price, max_price))]
    
    # Display the filtered DataFrame
    st.subheader(f"Items within rating range {min_rating} to {max_rating} and price range £{min_price} to £{max_price} in {selected_collection}")
    st.dataframe(filtered_df[['title', 'rating', 'price', 'inStock']], use_container_width=True)


    st.markdown("<hr>", unsafe_allow_html=True)  # Horizontal line
    st.markdown('<h2 style="text-align: center; color:darkblue;">Infographics</h2>', unsafe_allow_html=True)

   
    # Prepare data for the graphs
    # Graph 1: Count of IDs to Ratings
    rating_count = df['rating'].value_counts()

    # Graph 3: Total Count across all collections by collection names
    total_count_by_collection = {name: len(collection_data[name]) for name in collection_data.keys()}

    # Graph 4: Ratings vs Count of ID across all collections
    ratings_across_collections = pd.concat([col['rating'] for col in collection_data.values() if 'rating' in col.columns])
    ratings_count_across_collections = ratings_across_collections.value_counts()

    # Create the graphs
    fig1 = px.bar(rating_count, x=rating_count.index, y=rating_count.values, labels={'x': 'Rating', 'y': 'Count'}, title="Count of IDs to Ratings")
    fig3 = px.bar(x=list(total_count_by_collection.keys()), y=list(total_count_by_collection.values()), labels={'x': 'Collection', 'y': 'Total Count'}, title="Total Count by Collection")
    fig4 = px.bar(ratings_count_across_collections, x=ratings_count_across_collections.index, y=ratings_count_across_collections.values, labels={'x': 'Rating', 'y': 'Count'}, title="Ratings vs Count of ID Across Collections")

    # Display the graphs serially
    st.plotly_chart(fig1)
    # Add more charts here if needed
    st.plotly_chart(fig3)
    st.plotly_chart(fig4)
