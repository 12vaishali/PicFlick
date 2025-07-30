import os
import streamlit as st
from PIL import Image
import random

# Sample data for AR filters
ar_filters = [
    {
        "id": 1,
        "name":"Face Warp",
        "short_desc": "Distorts facial features in an exaggerated way.",
        "long_desc": "Applies real-time warping effects to your face, stretching, squishing, or otherwise exaggerating your features for a humorous effect. This filter is perfect for creating funny and silly content.",
        "image_url":"https://play-lh.googleusercontent.com/skspILPcvz4rxjETLXujZipYW8BV3zjxhqipLnyS-mAUybKQYIfSsLjikRVjmjn3NjyK=w240-h480-rw",
        "rating": 4.5,
        "link":"https://lens.snap.com/experience/8727455b-c7b9-4b88-b9a0-1639779c5129",
    },
    {
        "id": 2,
        "name":"Big Eye",
         "short_desc": "Enlarges the user's eyes for a cartoonish look.",
        "long_desc": "Dramatically increases the size of your eyes, creating a wide-eyed, cartoonish, and sometimes surreal appearance. This filter can evoke feelings of surprise, cuteness, or whimsy.",
        "image_url": "https://play-lh.googleusercontent.com/9MTaql19BpqhdGRuVFAXEZJiee4gGc-md8wugTkrLWkLrfQvFX_QnfJFax7sAVx7pUA",
        "rating": 4.2,
        "link":"https://lens.snap.com/experience/1863ad47-6a0c-46db-bd98-d0ed71d44f45"
    },

    {
        "id": 3,
        "name":"Green Eye",
       "short_desc": "Changes the user's eye color to green.",
        "long_desc": "Digitally alters the color of your eyes to various shades of green, enhancing your natural beauty or creating a more mysterious and alluring look. This filter can evoke feelings of enchantment and natural beauty.",
        "image_url": "https://lasikomaha.com/wp-content/uploads/2021/03/blog-KVgeneral-green-eye-facts_FeatureImg-copy.jpg",
        "rating": 4.5,
        "link":"https://lens.snap.com/experience/26333e32-0691-445c-bfb9-2da54cef38c8"
    },
    ]

# Custom CSS for styling
st.markdown("""
<style>
    .card {
        border: 1px solid #007bff;
        border-radius: 10px;
        padding: 15px;
        margin: 10px;
        transition: transform 0.2s;
        background-color: black;
        color: lightgrey;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .expanded-card {
        border: 1px solid #ddd;
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 1000;
        background:rgb(14, 17, 23);
        width: 60%;
        padding: 10px;
        border-radius: 15px;
        box-shadow: 0 0 20px rgba(0,0,0,0.2);
    }
    .sidebar .sidebar-content {
        transition: width 0.3s;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'sidebar_expanded' not in st.session_state:
    st.session_state.sidebar_expanded = False
if 'selected_filter' not in st.session_state:
    st.session_state.selected_filter = None

#customizing the sidebar
with st.sidebar:
    
    st.title("PicFlick : An enhanced AR experience")
    st.markdown("""
     **Instruction**: To search any filter, type the name of the filter in the search bar , insert a space and press ENTER.

    """)

def close_expanded_card():
        st.session_state.selected_filter = None
        
# Expanded card view
if st.session_state.selected_filter:
    filter = st.session_state.selected_filter
    
    # Check if the image is local or remote
    if filter['image_url'].startswith('http'):
        # Generate HTML with remote image
        card_html = f"""
        <div class="expanded-card">
            <div style="display: flex; gap: 20px; padding: 15px;">
                <div style="flex: 1;">
                    <img src="{filter['image_url']}" style="width: 100%; border-radius: 8px;">
                </div>
                <div style="flex: 2;">
                    <h2>{filter['name']}</h2>
                    <div style="margin: 10px 0;">
                        {"⭐" * int(filter["rating"])} ({filter["rating"]})
                    </div>
                    <p>{filter['long_desc']}</p>
                    <a href="{filter['link']}" target="_blank" style="padding: 10px 20px; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px; display: inline-block;">
                        OPEN FILTER
                    </a>
                </div>
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
    else:
        # Use st.columns for layout with local image
        st.button("Close The Currently Opened Card", on_click=close_expanded_card, key="close_outside_card")
        cols = st.columns([1, 2])
        with cols[0]:
            try:
                st.image(filter['image_url'])
            except Exception as e:
                st.error(f"Could not load image: {e}")
        
        with cols[1]:
            st.header(filter['name'])
            st.write("⭐" * int(filter["rating"]) + f" ({filter['rating']})")
            st.write(filter['long_desc'])
            st.markdown(f"[OPEN FILTER]({filter['link']})")

# Main content area
st.title("Face Deform")
st.subheader("Select a filter to apply to your video stream to see changes to your face in real-time")
st.divider()

# Filter cards display
if not st.session_state.selected_filter:
    cols = st.columns(3)
    for idx, filter in enumerate(ar_filters):
        with cols[idx % 3]:
            with st.container():
                # Check if the image URL is remote or local
                if filter['image_url'].startswith('http'):
                    # For web URLs, embed directly in HTML
                    st.markdown(f"""
                    <div class="card" onclick="window.streamlit.setComponentValue({filter['id']})">
                        <img src="{filter['image_url']}" width="100%" style="border-radius: 8px;">
                        <h3>{filter['name']}</h3>
                        <p>{filter['short_desc']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    # For local files, also embed directly in HTML
                    # Ensure the path is correct relative to the Streamlit app's root directory
                    st.markdown(f"""
                    <div class="card" onclick="window.streamlit.setComponentValue({filter['id']})">
                        <img src="{filter['image_url']}" width="100%" style="border-radius: 8px;">
                        <h3>{filter['name']}</h3>
                        <p>{filter['short_desc']}</p>
                    </div>
                    """, unsafe_allow_html=True)

                if st.button(f"Select {filter['name']}", key=filter['id']):
                    st.session_state.selected_filter = filter

# Expanded card view
if st.session_state.selected_filter:
    filter = st.session_state.selected_filter

    # Generate all HTML content as a single string
    card_html = f"""
    <div class="expanded-card">
        <div style="display: flex; gap: 20px; padding: 15px;">
            <div style="flex: 1;">
                <img src="{filter['image_url']}" style="width: 100%; border-radius: 8px;">
            </div>
             { st.button("Close The Currently Opened Card",on_click=close_expanded_card, key="close_outside_card")}
            <div style="flex: 2;">
                <h2>{filter['name']}</h2>
                <div style="margin: 10px 0;">
                    {"⭐" * int(filter["rating"])} ({filter["rating"]})
                </div>
                <p>{filter['long_desc']}</p>
                 <a href="{filter['link']}" target="_blank" style="padding: 10px 20px; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px; display: inline-block;">
                    OPEN FILTER
                </a>
            </div>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

with st.sidebar:
    search_query = st.text_input("🔍 Search Filters")
    if search_query:
        filtered_filters = [filter for filter in ar_filters if search_query.lower() in filter['name'].lower()]
        if filtered_filters:
            filter = filtered_filters[0]
            st.session_state.selected_filter = filter
            
        
  

            

