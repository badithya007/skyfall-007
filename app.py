import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="MiniStore | Modern E-Commerce Demo",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS INJECTION ---
st.markdown("""
<style>
    /* Global layout settings */
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
    
    /* Floating Chat Button styles */
    .floating-chat-container {
        position: fixed;
        bottom: 30px;
        right: 30px;
        z-index: 9999;
    }
</style>
""", unsafe_allow_html=True)

# --- INITIALIZE SESSION STATE ---
if 'cart' not in st.session_state:
    st.session_state.cart = {}

# --- SAMPLE PRODUCT DATA ---
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
    st.toast("Added item to cart! 🛒")

def clear_cart():
    st.session_state.cart = {}

# --- SIDEBAR: FILTERS & CART SUMMARY ---
with st.sidebar:
    st.title("📌 Navigation")
    
    categories = ["All Products"] + list(set(p["category"] for p in PRODUCTS))
    selected_category = st.selectbox("Browse by Category", categories)
    
    st.write("---")
    
    st.title("🛒 Your Cart")
    if not st.session_state.cart:
        st.info("Your shopping cart is empty.")
    else:
        total_cost = 0.0
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
        
        if st.button("Proceed to Checkout", type="primary", use_container_width=True):
            st.success("🎉 Order demo placed successfully!")
            clear_cart()
            
        if st.button("Clear Cart", type="secondary", use_container_width=True):
            clear_cart()
            st.rerun()

# --- MAIN CONTENT: HOMEPAGE ---
st.markdown("""
    <div class="hero-container">
        <h1>Welcome to MiniStore</h1>
        <p>Discover handpicked premium essentials crafted for your modern lifestyle.</p>
    </div>
""", unsafe_allow_html=True)

filtered_products = PRODUCTS if selected_category == "All Products" else [p for p in PRODUCTS if p["category"] == selected_category]
st.subheader(f"✨ Featured Products ({selected_category})")

cols_per_row = 3
for i in range(0, len(filtered_products), cols_per_row):
    row_products = filtered_products[i:i + cols_per_row]
    columns = st.columns(cols_per_row)
    
    for idx, product in enumerate(row_products):
        with columns[idx]:
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
            
            price_col, btn_col = st.columns([1, 1])
            with price_col:
                st.markdown(f"<div class='product-price'>${product['price']:.2f}</div>", unsafe_allow_html=True)
            with btn_col:
                st.button("Add to Cart", key=f"btn_{product['id']}", on_click=add_to_cart, args=(product['id'],), use_container_width=True)
            
            st.write("#")

# --- FLOATING SUPPORT BUTTON ---
# Implements a position:fixed wrapper container to draw an eye-catching button bridging over to the user support channel
st.markdown('<div class="floating-chat-container">', unsafe_allow_html=True)
if st.button("💬 Chat with Support", type="primary", help="Need assistance? Speak with our virtual support assistant."):
    st.switch_page("pages/1_Support_Chatbot.py")
st.markdown('</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 0.85rem;'>© 2026 MiniStore Inc. Built entirely with Streamlit.</p>", unsafe_allow_html=True)
import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="MiniStore Support Bot", page_icon="🤖", layout="centered")

st.title("🤖 MiniStore Virtual Assistant")
st.markdown("Ask me anything about our **products, orders, delivery, refunds, returns, or payment methods**.")

# --- PERSISTENT STORE CATALOG REFERENCE ---
# Used by parsing rules to fetch live inventory variables
PRODUCTS_INVENTORY = [
    {"name": "AeroFit Wireless Earbuds", "price": "$79.99", "details": "Noise-canceling, 30h battery life."},
    {"name": "Quantum Mechanical Keyboard", "price": "$129.50", "details": "RGB, tactile switches, aluminum top."},
    {"name": "Nomad Canvas Backpack", "price": "$65.00", "details": "Water-resistant canvas, 15\" laptop sleeve."},
    {"name": "Chronos Minimalist Watch", "price": "$145.00", "details": "Sapphire glass, genuine Italian leather."},
    {"name": "HydroPeak Stainless Flask", "price": "$32.00", "details": "32oz vacuum insulated flask, cold 24h."},
    {"name": "Lumio Smart Ambient Lamp", "price": "$49.99", "details": "App-controlled LED lamp, sunrise simulation."}
]

# --- INITIALIZE CHAT HISTORY ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your MiniStore assistant. How can I help you today?"}
    ]

# --- RULE-BASED RESPONSE ENGINE ---
def generate_support_response(user_query: str) -> str:
    query = user_query.lower()
    
    # Keyword Check 1: Product lookup queries
    if "product" in query or "item" in query or "stock" in query or "buy" in query:
        response = "We offer premium essentials! Here is our current catalog:\n\n"
        for p in PRODUCTS_INVENTORY:
            response += f"- **{p['name']}** ({p['price']}): {p['details']}\n"
        response += "\nYou can add any of these to your basket right from the main homepage dashboard."
        return response
    
    # Specific individual product checks
    for p in PRODUCTS_INVENTORY:
        if p['name'].split()[0].lower() in query: # Matches 'aerofit', 'quantum', 'nomad', etc.
            return f"The **{p['name']}** is priced at {p['price']}. Key features: {p['details']}"

    # Keyword Check 2: Deliveries
    if "delivery" in query or "shipping" in query or "ship" in query:
        return "📦 **Shipping Policy:** We provide free standard shipping across the country for all orders over $50. Standard deliveries typically arrive within 3-5 business days. Express shipping options are available at checkout."

    # Keyword Check 3: Refunds
    if "refund" in query:
        return "💰 **Refunds:** Once your return is received and inspected at our fulfillment center, we process refunds back to your original payment method within 5-7 business days."

    # Keyword Check 4: Returns
    if "return" in query:
        return "🔄 **Returns:** We offer a 30-day hassle-free return window on all unused items in original packaging. Please reach out to your tracking email link to generate a prepaid mailing return slip."

    # Keyword Check 5: Methods of Payment
    if "payment" in query or "pay" in query or "card" in query:
        return "💳 **Accepted Payments:** MiniStore securely accepts all major credit cards (Visa, MasterCard, American Express), Apple Pay, Google Pay, and PayPal."

    # Keyword Check 6: Tracking Status
    if "order" in query or "status" in query or "track" in query:
        return "🕵️‍♂️ **Order Tracking:** To track your purchase package, please input your 8-digit order identification reference ID into our global carrier terminal, or check the confirmation details dispatched directly to your inbox."

    # Default fallback response
    return "I am glad to assist, but I didn't quite catch that. Could you please specify your query? (e.g., ask me about 'returns', 'shipping timeline', or our 'wireless earbuds' product properties!)"


# --- RENDER CHAT HISTORY ELEMENTS ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- HANDLE NEW USER USER INPUT CONSOLE ---
if user_input := st.chat_input("Type your support request here..."):
    # Append and show User Message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
        
    # Generate, append, and show Assistant Response
    bot_reply = generate_support_response(user_input)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)

# --- BACK TO HOME NAVIGATION UTILITY ---
st.write("---")
if st.button("⬅️ Back to Storefront Homepage", use_container_width=True):
    st.switch_page("app.py")