import streamlit as st
import sqlite3
from PIL import Image

from auth import login, logout
from home import show_home
from farmer import farmer_dashboard
from customer import customer_dashboard
from cart import cart_page

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Farmer",
    page_icon="🌱",
    layout="wide"
)

# ---------------- DATABASE ----------------
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    role TEXT,
    UNIQUE(username, role)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS vegetables(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    farmer_name TEXT,
    vegetable_name TEXT,
    price REAL,
    quantity INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer TEXT,
    vegetable TEXT,
    quantity INTEGER,
    order_date TEXT
)
""")

conn.commit()

# ---------------- LANGUAGE ----------------
LANG = {
    "English": {
        "login":"Login",
        "username":"Username",
        "password":"Password",
        "role":"Login as",
        "farmer":"Farmer",
        "customer":"Customer",
        "logout":"Logout",
        "add_veg":"Add Vegetable",
        "veg_name":"Vegetable Name",
        "price":"Price (₹/Kg)",
        "qty":"Quantity (Kg)",
        "buy":"Buy",
        "order_history":"Order History",
        "no_orders":"No Orders Yet"
    },

    "தமிழ்": {
        "login":"உள்நுழைவு",
        "username":"பயனர் பெயர்",
        "password":"கடவுச்சொல்",
        "role":"உள்நுழைவு வகை",
        "farmer":"விவசாயி",
        "customer":"வாடிக்கையாளர்",
        "logout":"வெளியேறு",
        "add_veg":"காய்கறி சேர்க்க",
        "veg_name":"காய்கறி பெயர்",
        "price":"விலை (₹/கிலோ)",
        "qty":"அளவு (கிலோ)",
        "buy":"வாங்க",
        "order_history":"ஆர்டர் வரலாறு",
        "no_orders":"ஆர்டர் இல்லை"
    }
}

# ---------------- SESSION ----------------
if "user" not in st.session_state:
    st.session_state.user = None

if "role" not in st.session_state:
    st.session_state.role = None

if "cart" not in st.session_state:
    st.session_state.cart = []

# ---------------- SIDEBAR ----------------
language = st.sidebar.selectbox(
    "🌐 Language",
    ["English", "தமிழ்"]
)

T = LANG[language]

# ---------------- LOGO ----------------
try:
    logo = Image.open("assets/logo.png")
    st.sidebar.image(logo, width=180)
except:
    pass

st.sidebar.title("🌱 Smart Farmer")

# ---------------- HOME ----------------
show_home(cursor)

st.markdown("---")

# ---------------- LOGIN ----------------
if st.session_state.user is None:

    user, role = login(conn, cursor, T)

    if user:
        st.session_state.user = user
        st.session_state.role = role
        st.rerun()

# ---------------- AFTER LOGIN ----------------
else:

    st.sidebar.success(f"👋 {st.session_state.user}")

    if st.session_state.role == "Farmer":

        page = st.sidebar.radio(
            "Navigation",
            [
                "Farmer Dashboard"
            ]
        )

        if page == "Farmer Dashboard":
            farmer_dashboard(
                conn,
                cursor,
                st.session_state.user,
                T
            )

    else:

        page = st.sidebar.radio(
            "Navigation",
            [
                "Customer Dashboard",
                "Shopping Cart"
            ]
        )

        if page == "Customer Dashboard":
            customer_dashboard(
                conn,
                cursor,
                st.session_state.user,
                T
            )

        elif page == "Shopping Cart":
            cart_page(
                conn,
                cursor,
                st.session_state.user
            )

    st.sidebar.markdown("---")

    if st.sidebar.button("🚪 Logout", use_container_width=True):
        logout()

conn.close()