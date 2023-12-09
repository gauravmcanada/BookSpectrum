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
# Function to process collection data
def process_collection_data(collection):
    df = pd.DataFrame(list(collection.find()))
    df['price'] = df['price'].replace('[\£]', '', regex=True).astype(float)
    avg_price = df['price'].mean()
    num_ids = len(df)
    in_stock_count = df['inStock'].sum()
    return df, avg_price, num_ids, in_stock_count

# Streamlit app
st.title('MongoDB Collections Overview')

# Display collections and their overview
collection_data = {}
for name in db.list_collection_names():
    collection = db[name]
    df, avg_price, num_ids, in_stock_count = process_collection_data(collection)
    collection_data[name] = df
    st.write(f"{name}: Avg Price £{avg_price:.2f}, Total IDs: {num_ids}, In Stock: {in_stock_count}")
# Function to process collection data
def process_collection_data(collection):
    df = pd.DataFrame(list(collection.find()))
    df['price'] = df['price'].replace('[\£]', '', regex=True).astype(float)
    return df
# Function to process collection data
def process_collection_data(collection):
    df = pd.DataFrame(list(collection.find()))
    df['price'] = df['price'].replace('[\£]', '', regex=True).astype(float)
    return df

# Streamlit app
st.title('MongoDB Collections Analysis')

# Display collections and their overview
collection_data = {}
for name in db.list_collection_names():
    collection = db[name]
    df = process_collection_data(collection)
    collection_data[name] = df

# Interactivity on selecting a collection
selected_collection = st.selectbox("Select a collection to view details:", list(collection_data.keys()))
if selected_collection:
    df = collection_data[selected_collection]

    # Title filter
    title_filter = st.text_input("Filter by title:")
    if title_filter:
        filtered_df_title = df[df['title'].str.contains(title_filter, case=False, na=False)]
        st.subheader(f"Items matching title '{title_filter}' in {selected_collection}")
        st.dataframe(filtered_df_title)

    # Rating and price sliding filters
    min_rating, max_rating = st.slider("Filter by rating range:", 1, 5, (1, 5))
    min_price, max_price = st.slider("Filter by price range (£):", float(df['price'].min()), float(df['price'].max()), (float(df['price'].min()), float(df['price'].max())))

    # Assuming ratings are stored as 'One', 'Two', etc., in the collection
    rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    df['rating_numeric'] = df['rating'].map(rating_map)  # Map textual ratings to numeric

    filtered_df_rating_price = df[(df['rating_numeric'] >= min_rating) & (df['rating_numeric'] <= max_rating) & (df['price'].between(min_price, max_price))]
    st.subheader(f"Items within rating range {min_rating} to {max_rating} and price range £{min_price} to £{max_price} in {selected_collection}")
    st.dataframe(filtered_df_rating_price[['title', 'rating', 'price', 'inStock']])  # Display relevant columns

    # Graphs
    # Price vs. Rating
    fig1 = px.scatter(df, x="rating_numeric", y="price", title="Price vs. Rating")
    st.plotly_chart(fig1)

    # Rating vs. Count of IDs
    rating_count = df['rating'].value_counts()
    fig2 = px.bar(rating_count, x=rating_count.index, y=rating_count.values, labels={'x': 'Rating', 'y': 'Count'}, title="Rating vs. Count of IDs")
    st.plotly_chart(fig2)

 # In Stock vs. Out of Stock count graph
    in_stock_count = df['inStock'].value_counts()
    fig3 = px.bar(in_stock_count, x=in_stock_count.index, y=in_stock_count.values, labels={'x': 'In Stock', 'y': 'Count'}, title="In Stock vs. Out of Stock")
    st.plotly_chart(fig3)
# Note: Adjust the rating_map dictionary based on how ratings are stored in your MongoDB collection