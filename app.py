import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="MiniStore | Modern E-Commerce Demo",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS INJECTION ---
# Enhances the default Streamlit look with modern cards, clean typography, and vibrant buttons
st.markdown("""
<style>
    /* Global styles */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        color: #1E293B;
    }
    
    /* Hero Section */
    .hero-container {
        background: linear-gradient(135deg, #6366F1 0%, #4338CA 100%);
        padding: 3rem 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 2.5rem;
        text-align: center;
    }
    .hero-container h1 {
        color: white !important;
        font-size: 2.8rem !important;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .hero-container p {
        font-size: 1.2rem;
        opacity: 0.9;
    }

    /* Product Card Styling */
    .product-card {
        background-color: #FFFFFF;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border: 1px solid #E2E8F0;
        margin-bottom: 1.5rem;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .product-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
    .product-category {
        font-size: 0.75rem;
        text-transform: uppercase;
        color: #6366F1;
        font-weight: 700;
        letter-spacing: 0.05em;
        margin-bottom: 0.25rem;
    }
    .product-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #0F172A;
        margin-bottom: 0.5rem;
        min-height: 2.5rem;
    }
    .product-desc {
        color: #64748B;
        font-size: 0.9rem;
        line-height: 1.4;
        margin-bottom: 1rem;
        min-height: 4rem;
    }
    .product-price {
        font-size: 1.4rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 1rem;
    }
    
    /* Sidebar adjustments */
    .sidebar .sidebar-content {
        background-color: #F8FAFC;
    }
</style>
""", unsafe_allow_html=True)

# --- INITIALIZE SESSION STATE ---
# Used to persist shopping cart data across user interactions/reloads
if 'cart' not in st.session_state:
    st.session_state.cart = {}

# --- SAMPLE PRODUCT DATA ---
# 6 Realistic products spanning 3 categories
PRODUCTS = [
    {
        "id": 1,
        "name": "AeroFit Wireless Earbuds",
        "category": "Electronics",
        "price": 79.99,
        "description": "True wireless noise-canceling earbuds with 30-hour battery life and ergonomic sweatproof design.",
        "image": "🎧"
    },
    {
        "id": 2,
        "name": "Quantum Mechanical Keyboard",
        "category": "Electronics",
        "price": 129.50,
        "description": "Tactile RGB mechanical keyboard featuring hot-swappable switches and premium aluminum top plate.",
        "image": "⌨️"
    },
    {
        "id": 3,
        "name": "Nomad Canvas Backpack",
        "category": "Apparel & Accessories",
        "price": 65.00,
        "description": "Water-resistant, heavy-duty canvas pack with a dedicated 15-inch laptop sleeve and leather accents.",
        "image": "🎒"
    },
    {
        "id": 4,
        "name": "Chronos Minimalist Watch",
        "category": "Apparel & Accessories",
        "price": 145.00,
        "description": "Sleek, scratch-resistant sapphire glass analog watch paired with a genuine Italian leather band.",
        "image": "⌚"
    },
    {
        "id": 5,
        "name": "HydroPeak Stainless Flask",
        "category": "Home & Lifestyle",
        "price": 32.00,
        "description": "Double-wall vacuum insulated 32oz water bottle that keeps drinks ice-cold for up to 24 hours.",
        "image": "🧉"
    },
    {
        "id": 6,
        "name": "Lumio Smart Ambient Lamp",
        "category": "Home & Lifestyle",
        "price": 49.99,
        "description": "App-controlled LED bedside lamp capable of syncing with music and simulating natural sunrises.",
        "image": "💡"
    }
]

# --- CART FUNCTIONS ---
def add_to_cart(product_id):
    if product_id in st.session_state.cart:
        st.session_state.cart[product_id] += 1
    else:
        st.session_state.cart[product_id] = 1
    st.toast(f"Added item to cart! 🛒")

def clear_cart():
    st.session_state.cart = {}

# --- SIDEBAR: FILTERS & CART SUMMARY ---
with st.sidebar:
    st.title("📌 Navigation")
    
    # Category Filter
    categories = ["All Products"] + list(set(p["category"] for p in PRODUCTS))
    selected_category = st.selectbox("Browse by Category", categories)
    
    st.write("---")
    
    # Shopping Cart Section
    st.title("🛒 Your Cart")
    if not st.session_state.cart:
        st.info("Your shopping cart is empty.")
    else:
        total_cost = 0.0
        # Iterate over item IDs in session state and render items
        for prod_id, qty in list(st.session_state.cart.items()):
            product = next((p for p in PRODUCTS if p["id"] == prod_id), None)
            if product:
                item_total = product["price"] * qty
                total_cost += item_total
                st.markdown(f"**{product['image']} {product['name']}**")
                st.markdown(f"Qty: {qty} × ${product['price']:.2f} = **${item_total:.2f}**")
                st.write("")
        
        st.write("---")
        st.markdown(f"### Total: `${total_cost:.2f}`")
        
        # Checkout & Clear actions
        if st.button("Proceed to Checkout", type="primary", use_container_width=True):
            st.success("🎉 Order demo placed successfully!")
            clear_cart()
            
        if st.button("Clear Cart", type="secondary", use_container_width=True):
            clear_cart()
            st.rerun()

# --- MAIN CONTENT: HOMEPAGE ---

# Hero Banner
st.markdown("""
    <div class="hero-container">
        <h1>Welcome to MiniStore</h1>
        <p>Discover handpicked premium essentials crafted for your modern lifestyle.</p>
    </div>
""", unsafe_allow_html=True)

# Filter products based on selected category from Sidebar
filtered_products = PRODUCTS if selected_category == "All Products" else [p for p in PRODUCTS if p["category"] == selected_category]

st.subheader(f"✨ Featured Products ({selected_category})")

# Responsive Grid Layout Construction (3 items per row)
# Chunking the list into groups of 3
cols_per_row = 3
for i in range(0, len(filtered_products), cols_per_row):
    row_products = filtered_products[i:i + cols_per_row]
    columns = st.columns(cols_per_row)
    
    for idx, product in enumerate(row_products):
        with columns[idx]:
            # Render custom HTML styles card component
            st.markdown(f"""
                <div class="product-card">
                    <div>
                        <div style='font-size: 3rem; margin-bottom: 0.5rem;'>{product['image']}</div>
                        <div class="product-category">{product['category']}</div>
                        <div class="product-title">{product['name']}</div>
                        <div class="product-desc">{product['description']}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Sub-price layout with Add-To-Cart actions
            # Rendered using native Streamlit keys directly below the HTML block to preserve formatting and functionality
            price_col, btn_col = st.columns([1, 1])
            with price_col:
                st.markdown(f"<div class='product-price'>${product['price']:.2f}</div>", unsafe_allow_html=True)
            with btn_col:
                # Unique button tracking utilizing product IDs
                st.button("Add to Cart", key=f"btn_{product['id']}", on_click=add_to_cart, args=(product['id'],), use_container_width=True)
            
            st.write("#") # Visual spacer between row iterations

# --- FOOTER ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 0.85rem;'>© 2026 MiniStore Inc. Built entirely with Streamlit.</p>", unsafe_allow_html=True)