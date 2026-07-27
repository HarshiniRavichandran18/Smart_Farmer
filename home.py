import streamlit as st

# ---------------- HOME PAGE ----------------

def show_home(cursor):
    st.title("🌱 Smart Farmer")
    st.subheader("Fresh Vegetables Directly from Farmers")
    st.markdown(
        """
        **Fresh • Affordable • Secure**
        """
    )

    st.markdown("---")

    # ---------------- HERO BANNER ----------------
    st.markdown("""
    <div style="
        background: linear-gradient(90deg,#2e7d32,#66bb6a);
        padding:25px;
        border-radius:15px;
        color:white;
        text-align:center;
        margin-bottom:20px;">
        <h2>🥕 Buy Fresh Vegetables Online</h2>
        <p>Support Local Farmers • Get Fresh Produce at Your Doorstep</p>
    </div>
    """, unsafe_allow_html=True)

    # ---------------- FEATURES ----------------
    st.subheader("🌟 Why Choose Smart Farmer?")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.success("👨‍🌾\n\nDirect from Farmers")

    with col2:
        st.info("🚚\n\nFast Delivery")

    with col3:
        st.warning("💳\n\nSecure Payment")

    with col4:
        st.success("🌐\n\nTamil & English")

    st.markdown("---")

    # ---------------- AVAILABLE VEGETABLES ----------------
    st.subheader("🥬 Available Vegetables")

    cursor.execute("""
        SELECT vegetable_name, price, quantity
        FROM vegetables
        WHERE quantity > 0
        ORDER BY vegetable_name
    """)

    vegetables = cursor.fetchall()

    if vegetables:

        cols = st.columns(3)

        for index, veg in enumerate(vegetables):

            with cols[index % 3]:

                st.markdown(f"""
                <div style="
                background:white;
                padding:15px;
                border-radius:12px;
                box-shadow:0px 3px 8px rgba(0,0,0,0.15);
                margin-bottom:15px;
                ">
                <h4>🥬 {veg[0]}</h4>
                <p>💰 ₹ {veg[1]} / Kg</p>
                <p>📦 Stock : {veg[2]} Kg</p>
                </div>
                """, unsafe_allow_html=True)

    else:
        st.info("No vegetables available.")

    st.markdown("---")

    # ---------------- TRENDING ----------------
    st.subheader("🔥 High Demand Vegetables")

    cursor.execute("""
        SELECT vegetable,
               SUM(quantity) AS sold
        FROM orders
        GROUP BY vegetable
        ORDER BY sold DESC
        LIMIT 5
    """)

    trending = cursor.fetchall()

    if trending:

        for veg in trending:
            st.write(f"🔥 **{veg[0]}**  —  {veg[1]} Kg Sold")

    else:
        st.info("No sales yet.")

    st.markdown("---")

    # ---------------- STATISTICS ----------------
    st.subheader("📊 Smart Farmer Statistics")

    cursor.execute("SELECT COUNT(*) FROM users WHERE role='Farmer'")
    farmers = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM users WHERE role='Customer'")
    customers = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM vegetables")
    products = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM orders")
    orders = cursor.fetchone()[0]

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("👨‍🌾 Farmers", farmers)

    with c2:
        st.metric("🛒 Customers", customers)

    with c3:
        st.metric("🥬 Vegetables", products)

    with c4:
        st.metric("📦 Orders", orders)

    st.markdown("---")

    st.success("🌱 Together we empower farmers and provide fresh vegetables to every home.")