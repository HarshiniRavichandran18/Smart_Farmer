import streamlit as st
from datetime import datetime


def cart_page(conn, cursor, username):

    st.title("🛒 Shopping Cart")

    if "cart" not in st.session_state:
        st.session_state.cart = []

    if len(st.session_state.cart) == 0:
        st.info("Your cart is empty.")
        return

    total = 0

    st.subheader("🧾 Order Summary")

    for i, item in enumerate(st.session_state.cart):

        subtotal = item["price"] * item["qty"]
        total += subtotal

        with st.container(border=True):

            col1, col2 = st.columns([5,1])

            with col1:
                st.write(f"🥬 **{item['name']}**")
                st.write(f"👨‍🌾 Farmer : {item['farmer']}")
                st.write(f"⚖ Quantity : {item['qty']} Kg")
                st.write(f"💰 ₹{item['price']} / Kg")
                st.write(f"💵 Subtotal : ₹{subtotal:.2f}")

            with col2:

                if st.button("❌ Remove", key=f"remove_{i}"):

                    st.session_state.cart.pop(i)
                    st.rerun()

    st.markdown("---")

    delivery_charge = 2 if total > 0 else 0

    grand_total = total + delivery_charge

    st.subheader("💳 Final Bill")

    st.write(f"🛍 Items Total : ₹{total:.2f}")
    st.write(f"🚚 Delivery Charge : ₹{delivery_charge:.2f}")

    st.success(f"### Grand Total : ₹{grand_total:.2f}")

    payment = st.selectbox(
        "Select Payment Method",
        [
            "Cash on Delivery",
            "UPI",
            "Debit Card",
            "Credit Card"
        ]
    )

    if st.button("✅ Place Order"):

        for item in st.session_state.cart:

            # Check stock
            cursor.execute(
                "SELECT quantity FROM vegetables WHERE id=?",
                (item["id"],)
            )

            available = cursor.fetchone()

            if available is None:
                st.error(f"{item['name']} not found.")
                return

            if available[0] < item["qty"]:
                st.error(
                    f"Only {available[0]} Kg of {item['name']} available."
                )
                return

        # Save all orders
        for item in st.session_state.cart:

            cursor.execute(
                """
                INSERT INTO orders
                (
                    customer,
                    vegetable,
                    quantity,
                    order_date
                )
                VALUES
                (?,?,?,?)
                """,
                (
                    username,
                    item["name"],
                    item["qty"],
                    datetime.now().strftime("%d-%m-%Y %H:%M")
                )
            )

            cursor.execute(
                """
                UPDATE vegetables
                SET quantity = quantity - ?
                WHERE id = ?
                """,
                (
                    item["qty"],
                    item["id"]
                )
            )

        conn.commit()

        st.success("🎉 Order Placed Successfully!")

        st.balloons()

        st.info(f"""
Payment Method : {payment}

Total Amount : ₹{grand_total:.2f}

Thank you for shopping with Smart Farmer 🌱
""")

        st.session_state.cart = []

        st.rerun()

    st.markdown("---")

    st.subheader("📜 My Order History")

    cursor.execute("""
        SELECT vegetable,
               quantity,
               order_date
        FROM orders
        WHERE customer=?
        ORDER BY id DESC
    """,(username,))

    orders = cursor.fetchall()

    if orders:

        for order in orders:

            with st.container(border=True):

                st.write(f"🥬 {order[0]}")
                st.write(f"⚖ {order[1]} Kg")
                st.write(f"📅 {order[2]}")

    else:

        st.info("No orders placed yet.")