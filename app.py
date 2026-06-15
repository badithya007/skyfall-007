import importlib
import importlib.util
import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="MiniStore Support Bot", page_icon="🤖", layout="centered")

st.title("🤖 MiniStore AI Assistant")
st.markdown("Ask me anything about our **products, delivery schedules, order tracking, refunds, or payment modes**.")

# --- CHECK OPENAI PACKAGE AVAILABILITY ---
if importlib.util.find_spec("openai") is None:
    st.error("The OpenAI Python package is not installed. Please install it with `pip install openai`.")
    st.stop()

openai = importlib.import_module("openai")
OpenAI = openai.OpenAI

# --- INITIALIZE OPENAI CLIENT ---
# This pulls the token seamlessly from your secure .streamlit/secrets.toml file
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- DEFINE STORE SYSTEM KNOWLEDGE & SCOPE CONSTRAINTS ---
SYSTEM_PROMPT = """
You are a highly professional, polite, and helpful customer support representative for 'MiniStore', an online e-commerce website.

Here is the exact live product catalog you must use to answer inventory questions:
1. AeroFit Wireless Earbuds | Price: $79.99 | Category: Electronics | Details: Noise-canceling, 30h battery life, sweatproof.
2. Quantum Mechanical Keyboard | Price: $129.50 | Category: Electronics | Details: RGB, tactile hot-swappable switches, aluminum plate.
3. Nomad Canvas Backpack | Price: $65.00 | Category: Apparel & Accessories | Details: Water-resistant canvas, 15" laptop sleeve, leather accents.
4. Chronos Minimalist Watch | Price: $145.00 | Category: Apparel & Accessories | Details: Sapphire glass, genuine Italian leather band.
5. HydroPeak Stainless Flask | Price: $32.00 | Category: Home & Lifestyle | Details: 32oz volume, double-wall vacuum insulated, keeps cold for 24h.
6. Lumio Smart Ambient Lamp | Price: $49.99 | Category: Home & Lifestyle | Details: App-controlled LED lamp, music sync, sunrise simulation.

Store Policies to follow:
- Delivery: Free standard shipping on orders over $50. Deliveries take 3-5 business days.
- Returns: 30-day hassle-free returns on unused items in original packaging.
- Refunds: Processed within 5-7 business days back to the original payment method after inspection.
- Payments: Accepts Visa, MasterCard, Amex, Apple Pay, Google Pay, and PayPal.

CRITICAL GUARDRAIL CONSTRAINTS:
- You are only allowed to answer questions related to MiniStore (products, inventory, ordering, delivery, refunds, returns, operations, or payments).
- If the user asks about ANYTHING outside of these e-commerce boundaries (e.g., coding, writing essays, recipes, mathematical calculations, general knowledge, or news), you must politely refuse to answer and redirect them to ask about store-related topics.
- Keep your tone concise, warm, and helpful.
"""

# --- INITIALIZE CHAT HISTORY (SESSION STATE) ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your MiniStore AI assistant. How can I help you with your order or products today?"}
    ]

# --- RENDER CHAT HISTORY FROM SESSION STATE ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- CONVERSATIONAL INPUT HANDLE ---
if user_input := st.chat_input("How can we help you today?"):
    
    # 1. Append and display the User's input prompt
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2. Query the OpenAI Chat Completion Endpoint
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Build full contextual payload including the System Constraints + History
        api_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + [
            {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
        ]
        
        try:
            # Request streaming generation from the modern model
            response = client.chat.completions.create(
                model="gpt-4o-mini", # Cost-effective, lightning-fast model for support pipelines
                messages=api_messages,
                temperature=0.3,     # Kept low to enforce strict adherence to documentation facts
            )
            
            bot_reply = response.choices[0].message.content
            message_placeholder.markdown(bot_reply)
            
            # 3. Save assistant reply to memory history array
            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            
        except Exception as e:
            st.error(f"Error communicating with OpenAI API: {str(e)}")

# --- UTILITY HOME BUTTON NAVIGATION ---
st.write("---")
if st.button("⬅️ Back to Storefront Homepage", use_container_width=True):
    st.switch_page("app.py")