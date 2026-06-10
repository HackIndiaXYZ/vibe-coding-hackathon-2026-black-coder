import streamlit as st
from google import genai
from google.genai import types

# UI Config & Styling (Premium Look)
st.set_page_config(page_title="OmniCare Real AI", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #f7f9fa; }
    .bot-btn {
        display: inline-block;
        padding: 12px 24px;
        background-color: #25D366;
        color: white !important;
        text-decoration: none;
        border-radius: 8px;
        font-weight: bold;
        margin: 10px 5px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 OmniCare AI - Real Voice & Chat Support")
st.write("### HackIndia 2026 Live Submission Platform")
st.info("💡 Yeh Bot official brand website se live price dekh kar customer ko help karta hai.")

# 1. API Setup (Streamlit Secrets se key load hogi)
API_KEY = st.secrets["GEMINI_API_KEY"] 
client = genai.Client(api_key=API_KEY)

# 2. Real AI Number 
real_ai_number = "0017164779375" 

# Sidebar Credits & Controls
st.sidebar.header("⚙️ Live System Status")
st.sidebar.success("Voice Server: ACTIVE 🟢")
st.sidebar.write(f"**Real AI Number:** `{real_ai_number}`")

# Clear Chat / Reset System Button
if st.sidebar.button("🧹 Clear Chat / New Customer"):
    st.session_state.messages = []
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("👑 Project Credits")
st.sidebar.write("**Lead Developer:** Prachi Agrawal")
st.sidebar.write("**Event:** HackIndia VIBE CODING 2026")

# 3. Universal System Prompt
strict_instruction = f"""
Tum ek Universal AI Customer Support Agent ho jo duniya ke sabhi brands ke liye kaam karta hai. Tumhara naam OmniCare AI hai.

HACKATHON & CREATOR CREDITS:
1. Tumhe 'Prachi Agrawal' ne specially HackIndia VIBE CODING HACKATHON 2026 ke liye banaya hai.
2. Agar koi pooche 'Tumhe kisne banaya?', 'Creator kaun hai?', ya 'Developer kaun hai?', toh proud hokar bolo: 
   "Mujhe Prachi Agrawal ne HackIndia VIBE CODING HACKATHON 2026 ke liye Vibe Coding workflow se banaya hai. Hum yeh hackathon jeetne ke liye poori tarah taiyar hain! 🚀"

SAFETY & UNIVERSAL SUPPORT RULES:
1. Tumhe hamesha USER SE HINDI YA HINGLISH mein hi baat karni hai. Polite aur professional raho.
2. User jis bhi brand ya product ke baare mein pooche, tum turant Google Search Grounding tool ka use karke us brand ki OFFICIAL WEBSITE par jao aur LIVE keemat dekh kar batao.
3. SECURITY RULE: Tumhe chat ke andar koi direct bank account, UPI ID, ya QR code nahi dena hai taaki koi dhoka-dhadi na ho.
4. JAB BHI CUSTOMER KHARIDNA (BUY) CHAHE, toh unhe saaf-saaf bolo: 
   "Aap kharidne ke liye niche diye gaye official link par jaakar ise safe tarike se buy kar sakte hain, ya fir hamare real AI number {real_ai_number} par call karke direct sahayata le sakte hain."
5. Tum jo bhi jankari do, uske sath Google Search se mili official website ka URL (link) customer ko zaroor do taaki woh khud check kar sakein.
6. Agar user kahe ki use call par baat karni hai, order lagwana hai, ya unhe koi complaint karni ho, toh bolo: 
   "Aap hamare real AI care number {real_ai_number} par call karke direct sahayata le sakte hain aur order book karwa sakte hain."
"""

# Chat memory management
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat logs
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)
        if "action_buttons" in message:
            st.markdown(message["action_buttons"], unsafe_allow_html=True)

# 4. User Interaction (Chat Input)
if user_question := st.chat_input("Kisi bhi brand ya product ka naam aur sawal likhein..."):
    st.session_state.messages.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.write(user_question)

    # Gemini Response Processing
    with st.chat_message("assistant"):
        with st.spinner("Official brand website se live aur safe data nikal raha hoon..."):
            grounding_tool = types.Tool(google_search=types.GoogleSearch())
            
            # Formatted Chat History Packaging
            formatted_contents = []
            for msg in st.session_state.messages[:-1]:
                role_type = "user" if msg["role"] == "user" else "model"
                formatted_contents.append(types.Content(
                    role=role_type,
                    parts=[types.Part.from_text(text=msg["content"])]
                ))
            
            formatted_contents.append(types.Content(
                role="user",
                parts=[types.Part.from_text(text=user_question)]
            ))
            
            try:
                response = client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=formatted_contents,
                    config=types.GenerateContentConfig(
                        system_instruction=strict_instruction,
                        tools=[grounding_tool],
                        temperature=0.2
                    )
                )
                bot_reply = response.text if response.text else "Maaf kijiyega, main abhi is jankari ko dhoondh nahi pa raha hoon."
            except Exception as e:
                bot_reply = "Technical issue ke karan response nahi mil paya. Kripya hamare direct number par sampark karein."
                
            st.markdown(bot_reply)
            
            msg_data = {"role": "assistant", "content": bot_reply}
            buttons_html = ""

            combined_text = (user_question + " " + bot_reply).lower()
            
            # Call Routing Feature (Green Button)
            if any(w in combined_text for w in ["call", "baat", "number", "phone", "contact", "order", "shikayat", "complaint"]):
                buttons_html += f'<a href="tel:{real_ai_number}" class="bot-btn">📞 Click To Call Real AI ({real_ai_number})</a>'

            # Website Redirect Feature (Blue Button)
            if any(w in combined_text for w in ["pay", "payment", "buy", "kharid", "lele", "link", "website", "price", "daam"]):
                search_query_encoded = user_question.replace(" ", "+")
                buttons_html += f'<a href="https://google.com{search_query_encoded}" target="_blank" class="bot-btn" style="background-color:#007bff;">🌐 Official Search Page Par Jayein</a>'

            if buttons_html:
                st.markdown(buttons_html, unsafe_allow_html=True)
                msg_data["action_buttons"] = buttons_html

            st.session_state.messages.append(msg_data)
