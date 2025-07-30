import os
import streamlit as st
from PIL import Image
import random

# Sample data for AR filters
ar_filters = [
    {
        "id": 1,
        "name":"Snow Effect",
        "short_desc": "Adds falling snow to the scene.",
        "long_desc": "Overlays realistic falling snow on your camera view, creating a serene and wintery atmosphere. Perfect for capturing cozy moments or adding a touch of magic to your surroundings.",
        "image_url":"https://p.bdir.in/img/jQuery-Plugin-For-Snowfall-Effect-with-Rotating-Snowflakes.png",
        "rating": 4.5,
        "link":"https://lens.snap.com/experience/d808edde-70e2-4d35-91b4-49ca8b5e2a65",
    },
    {
        "id": 2,
        "name":"Blurred Edge",
        "short_desc": "Blurs the edges of the view to focus on the center.",
        "long_desc": "Applies a soft blur effect to the periphery of your camera view, drawing attention to the central subject. This filter can create a dreamy, artistic, or introspective feel to your photos and videos.",
        "image_url": "https://d1hjkbq40fs2x4.cloudfront.net/2016-07-11/files/slow-shutter-sample_1304.jpg",
        "rating": 4.2,
        "link":"https://lens.snap.com/experience/a24df3e9-717f-4e7d-9fd5-66c097068b4d"
    },

    {
        "id": 3,
        "name":"Rain Effect",
        "short_desc": "Simulates a rainy day with visual and sometimes audio effects.",
        "long_desc": "Overlays realistic rain droplets on your screen, often accompanied by the subtle sound of rain, to create a melancholic, reflective, or cozy ambiance. Ideal for artistic expression or setting a specific mood.",
        "image_url": "https://freerangestock.com/sample/25037/raining-light-effect.jpg",
        "rating": 4.5,
        "link":"https://lens.snap.com/experience/b5527b3b-32f2-4d2d-b16e-6581031baa9d"
    },

    {
        "id": 4,
        "name":"Distorted Wave Effect",
        "short_desc": "Creates a wavy or rippling distortion across the image.",
        "long_desc": "Applies a dynamic wave-like distortion to your camera feed, producing a fluid, unreal, and sometimes psychedelic visual effect. Great for adding a unique and dynamic touch to your content.",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRjnr0XEExr7CU0Pa22oPHutMre9fWUKWxIBBpMtL1fTW3LR1_WUrzS8F6jtNHb2sv-o6I&usqp=CAU",
        "rating": 4.5,
        "link":"https://lens.snap.com/experience/a841107c-7f8a-4724-989f-a8db8bc54c83"
    }
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
st.title("Overlays")
st.subheader("Select a filter to apply to your video to see changes in your environment in real-time")
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
            
        
  

            

