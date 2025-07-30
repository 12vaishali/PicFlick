import streamlit as st
import pandas as pd
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Gemini model
def get_sentiment_model():
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.3,
        google_api_key=os.getenv("GOOGLE_API_KEY")  # From .env file
    )

# Process conversation history with error handling
def analyze_conversation(chat_history):
    llm = get_sentiment_model()
    
    user_messages = [msg["user"] for msg in chat_history]
    bot_responses = [msg["chatbot"] for msg in chat_history]
    
    prompt = f"""Analyze this customer support conversation. Return JSON with:
- overall_score: float between -1 (negative) and 1 (positive)
- dominant_emotion: string from [frustrated, satisfied, confused, neutral, angry]
- top_positive: most positive user message text
- top_negative: most negative user message text
- sentiment_trend: list of floats representing score for each message pair

Example valid response:
{{
    "overall_score": 0.45,
    "dominant_emotion": "frustrated",
    "top_positive": "Thanks for the quick resolution!",
    "top_negative": "This service is terrible!",
    "sentiment_trend": [0.2, -0.5, 0.8]
}}

Conversation History:
User Messages: {user_messages}
Agent Responses: {bot_responses}

Return only plain JSON without any formatting or comments:"""
    
    try:
        response = llm.invoke(prompt)
        # Clean response from markdown artifacts
        json_str = response.content.replace('```json', '').replace('```', '').strip()
        
        analysis = json.loads(json_str)
        
        # Validate response structure
        required_keys = ["overall_score", "dominant_emotion", 
                        "top_positive", "top_negative", "sentiment_trend"]
        if not all(key in analysis for key in required_keys):
            raise ValueError("Missing required keys in analysis response")
            
        # Convert to pandas series
        analysis["sentiment_trend"] = pd.Series(analysis["sentiment_trend"])
        
        return analysis
        
    except json.JSONDecodeError as e:
        st.error(f"JSON Parsing Error: {str(e)}")
        st.text("Raw Model Response:")
        st.code(response.content)
        return None
    except Exception as e:
        st.error(f"Analysis Error: {str(e)}")
        return None

# Main UI Components
def main():
    st.title("📈 Conversation Insights")
    
    if "chat_history" not in st.session_state or len(st.session_state.chat_history) < 1:
        st.warning("No conversation history found! Start chatting on the Home page.")
        return
    
    with st.spinner("Analyzing conversation patterns..."):
        analysis = analyze_conversation(st.session_state.chat_history)
    
    if not analysis:
        return
    
    # Metrics Row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Overall Sentiment", 
                f"{analysis['overall_score']:.2f}",
                help="-1 (Negative) to 1 (Positive)")
    
    with col2:
        st.metric("Dominant Emotion", 
                analysis["dominant_emotion"].title(),
                help="Most frequent emotion detected")
    
    with col3:
        st.metric("Conversation Turns", 
                len(st.session_state.chat_history))
    
    # Sentiment Timeline
    st.subheader("Sentiment Progression")
    st.line_chart(analysis["sentiment_trend"], 
                use_container_width=True,
                color="#4B77BE")
    
    # Key Messages Section
    st.subheader("Notable Interactions")
    
    col_left, col_right = st.columns(2)
    with col_left:
        with st.expander("🌟 Most Positive Interaction", expanded=True):
            if analysis["top_positive"]:
                st.markdown(f"**User:** {analysis['top_positive']}")
                corresponding_response = next(
                    msg["chatbot"] for msg in st.session_state.chat_history
                    if msg["user"] == analysis["top_positive"]
                )
                st.markdown(f"**Agent:** {corresponding_response}")
            else:
                st.info("No positive interactions detected")
    
    with col_right:
        with st.expander("⚠️ Most Negative Interaction", expanded=True):
            if analysis["top_negative"]:
                st.markdown(f"**User:** {analysis['top_negative']}")
                corresponding_response = next(
                    msg["chatbot"] for msg in st.session_state.chat_history
                    if msg["user"] == analysis["top_negative"]
                )
                st.markdown(f"**Agent:** {corresponding_response}")
            else:
                st.info("No negative interactions detected")
    
    # Debug Section
    with st.expander("Technical Details"):
        st.write("### Raw Analysis Data")
        st.json(analysis)
        st.write("### Conversation History")
        st.write(st.session_state.chat_history)

if __name__ == "__main__":
    main()