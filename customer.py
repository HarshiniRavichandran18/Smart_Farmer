import streamlit as st


def customer_dashboard(conn, cursor, username, T):
    st.title("🛒 Customer Dashboard")

    # ---------------- SEARCH ----------------
    search = st.text_input("🔍 Search Vegetable")

    if search:
        cursor.execute("""
            SELECT *
            FROM vegetables
            WHERE quantity > 0
            AND vegetable_name LIKE ?
            ORDER BY vegetable_name
        """, ('%' + search + '%',))
    else:
        cursor.execute("""
            SELECT *
            FROM vegetables
            WHERE quantity > 0
            ORDER BY vegetable_name
        """)

    vegetables = cursor.fetchall()

    if not vegetables:
        st.info("No vegetables available.")
        return

    # ---------------- CART ----------------
    if "cart" not in st.session_state:
        st.session_state.cart = []

    st.subheader("🥬 Fresh Vegetables")

    for veg in vegetables:

        with st.container(border=True):

            st.markdown(f"### 🥬 {veg[2]}")
            st.write(f"👨‍🌾 Farmer : {veg[1]}")
            st.write(f"💰 Price : ₹{veg[3]} / Kg")
            st.write(f"📦 Available : {veg[4]} Kg")

            qty = st.number_input(
                "Quantity (Kg)",
                min_value=1,
                max_value=int(veg[4]),
                value=1,
                key=f"qty_{veg[0]}"
            )

            if st.button("🛒 Add to Cart", key=f"cart_{veg[0]}"):

                found = False

                for item in st.session_state.cart:

                    if item["id"] == veg[0]:
                        item["qty"] += qty
                        found = True
                        break

                if not found:

                    st.session_state.cart.append({

                        "id": veg[0],
                        "name": veg[2],
                        "farmer": veg[1],
                        "price": veg[3],
                        "qty": qty

                    })

                st.success(f"{veg[2]} added to cart.")

    st.markdown("---")

    # ---------------- CART PREVIEW ----------------

    st.subheader("🛒 Cart Preview")

    if len(st.session_state.cart) == 0:

        st.info("Your cart is empty.")

    else:

        total = 0

        for i, item in enumerate(st.session_state.cart):

            subtotal = item["price"] * item["qty"]

            total += subtotal

            col1, col2 = st.columns([5, 1])

            with col1:

                st.write(
                    f"🥬 **{item['name']}** "
                    f"| {item['qty']} Kg "
                    f"| ₹{subtotal:.2f}"
                )

            with col2:

                if st.button("❌", key=f"remove{i}"):

                    st.session_state.cart.pop(i)

                    st.rerun()

        st.markdown("---")

        st.success(f"💰 Cart Total : ₹{total:.2f}")

        st.info("Proceed to Checkout from the Cart page.")