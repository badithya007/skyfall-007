import importlib
import importlib.util

if importlib.util.find_spec("streamlit") is not None:
    st = importlib.import_module("streamlit")
else:
    # Provide a lightweight stub to fail fast with a clear message when Streamlit
    # is not available (e.g., in linting or non-Streamlit environments).
    class _MissingStreamlit:
        def __getattr__(self, name):
            def _missing(*args, **kwargs):
                raise RuntimeError("Streamlit is required to run this app. Install it with: pip install streamlit")
            return _missing

    st = _MissingStreamlit()
import requests
from datetime import datetime

# --- CONFIGURATION & CONSTANTS ---
API_KEY = "a3f417b116fa4104b3c547e8ee9d32e1"
BASE_URL = "https://newsapi.org/v2/top-headlines"

# Streamlit Page Config
st.set_page_config(
    page_title="Global Pulse | Advanced News Dashboard",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- MAPPINGS FOR FILTERS ---
COUNTRIES = {
    "United States": "us",
    "United Kingdom": "gb",
    "India": "in",
    "Canada": "ca",
    "Australia": "au",
    "Germany": "de",
    "Japan": "jp",
    "France": "fr"
}

CATEGORIES = [
    "general", 
    "business", 
    "entertainment", 
    "health", 
    "science", 
    "sports", 
    "technology"
]

# --- FETCH DATA FUNCTION ---
def fetch_news(country_code, category, keyword, max_results):
    """Fetches news from NewsAPI based on user filters."""
    params = {
        "apiKey": API_KEY,
        "pageSize": max_results
    }
    
    # NewsAPI strict rule: You cannot mix 'country' or 'category' with the 'q' (keyword) 
    # parameter if searching globally, but top-headlines allows combining them.
    if country_code:
        params["country"] = country_code
    if category:
        params["category"] = category
    if keyword:
        params["q"] = keyword

    try:
        response = requests.get(BASE_URL, params=params)
        
        if response.status_code == 200:
            return response.json().get("articles", [])
        elif response.status_code == 401:
            st.error("🔒 Invalid API Key. Please check your credentials.")
            return []
        elif response.status_code == 429:
            st.error("⏳ Rate limit exceeded. Please try again later.")
            return []
        else:
            st.error(f"⚠️ Error {response.status_code}: {response.json().get('message', 'Unknown Error')}")
            return []
            
    except requests.exceptions.RequestException as e:
        st.error(f"📡 Connection Error: {e}")
        return []

# --- UI LAYOUT ---

# Header
st.title("📰 Global Pulse")
st.subheader("Advanced Real-Time News Analytics Dashboard")
st.markdown("---")

# Sidebar Filters
st.sidebar.header("🔍 Filter Options")

keyword_search = st.sidebar.text_input(
    "Search Keywords", 
    placeholder="e.g., AI, Stocks, Election..."
)

selected_country = st.sidebar.selectbox(
    "Select Location/Country", 
    options=["All"] + list(COUNTRIES.keys())
)

selected_category = st.sidebar.selectbox(
    "Select Topic/Category", 
    options=["All"] + [c.capitalize() for c in CATEGORIES]
)

num_articles = st.sidebar.slider(
    "Number of Articles", 
    min_value=5, 
    max_value=50, 
    value=15, 
    step=5
)

# Process Filter Inputs
country_param = COUNTRIES[selected_country] if selected_country != "All" else None
category_param = selected_category.lower() if selected_category != "All" else None

# Fetch Data Trigger
if st.sidebar.button("Fetch Latest News", type="primary"):
    with st.spinner("Fetching breaking news..."):
        articles = fetch_news(
            country_code=country_param, 
            category=category_param, 
            keyword=keyword_search, 
            max_results=num_articles
        )
        
    if articles:
        st.success(f"Found {len(articles)} articles matching your criteria.")
        
        # Display articles in a clean grid/list layout
        for idx, article in enumerate(articles):
            title = article.get("title", "No Title Available")
            description = article.get("description", "No description available for this article.")
            url = article.get("url", "#")
            image_url = article.get("urlToImage")
            source = article.get("source", {}).get("name", "Unknown Source")
            published_at = article.get("publishedAt", "")
            
            # Format Date
            if published_at:
                try:
                    date_obj = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")
                    formatted_date = date_obj.strftime("%b %d, %Y | %I:%M %p")
                except ValueError:
                    formatted_date = published_at
            else:
                formatted_date = "Unknown Date"

            # Render Article Card
            with st.container():
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    if image_url:
                        st.image(image_url, use_container_width=True)
                    else:
                        # Placeholder image if none exists
                        st.image("https://placehold.co/600x400?text=No+Image", use_container_width=True)
                        
                with col2:
                    st.markdown(f"### [{title}]({url})")
                    st.markdown(f"**Source:** `{source}` | **Published:** *{formatted_date}*")
                    st.write(description)
                    st.markdown(f"[Read full article]({url})")
                
                st.markdown("---")
    else:
        st.info("No articles found. Try adjusting your filters or keywords.")
else:
    st.info("👈 Use the sidebar filters and click **'Fetch Latest News'** to populate the dashboard.")