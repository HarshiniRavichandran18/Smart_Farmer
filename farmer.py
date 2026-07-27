import streamlit as st

def farmer_dashboard(conn, cursor, username, T):

    st.title("👨‍🌾 Farmer Dashboard")

    st.markdown("### ➕ Add New Vegetable")

    veg = st.text_input(T["veg_name"])
    price = st.number_input(T["price"], min_value=1)
    qty = st.number_input(T["qty"], min_value=1)

    if st.button(T["add_veg"]):

        if veg.strip() == "":
            st.warning("Please enter vegetable name.")

        else:

            cursor.execute("""
                INSERT INTO vegetables
                (farmer_name, vegetable_name, price, quantity)
                VALUES(?,?,?,?)
            """, (username, veg.title(), price, qty))

            conn.commit()

            st.success("✅ Vegetable Added Successfully!")

            st.rerun()

    st.markdown("---")

    st.subheader("🥬 My Vegetables")

    cursor.execute("""
        SELECT id, vegetable_name, price, quantity
        FROM vegetables
        WHERE farmer_name=?
        ORDER BY id DESC
    """, (username,))

    vegetables = cursor.fetchall()

    if not vegetables:
        st.info("No vegetables added yet.")

    for veg in vegetables:

        with st.container(border=True):

            st.write(f"### 🥬 {veg[1]}")
            st.write(f"💰 Price : ₹{veg[2]} / Kg")
            st.write(f"📦 Stock : {veg[3]} Kg")

            col1, col2 = st.columns(2)

            with col1:

                if st.button("✏ Edit", key=f"edit{veg[0]}"):

                    st.session_state["edit_id"] = veg[0]

            with col2:

                if st.button("🗑 Delete", key=f"delete{veg[0]}"):

                    cursor.execute(
                        "DELETE FROM vegetables WHERE id=?",
                        (veg[0],)
                    )

                    conn.commit()

                    st.success("Deleted Successfully")

                    st.rerun()

            if st.session_state.get("edit_id") == veg[0]:

                st.markdown("#### Update Vegetable")

                new_price = st.number_input(
                    "New Price",
                    value=int(veg[2]),
                    key=f"price{veg[0]}"
                )

                new_qty = st.number_input(
                    "New Quantity",
                    value=int(veg[3]),
                    key=f"qty{veg[0]}"
                )

                c1, c2 = st.columns(2)

                with c1:

                    if st.button("Save", key=f"save{veg[0]}"):

                        cursor.execute("""
                            UPDATE vegetables
                            SET price=?, quantity=?
                            WHERE id=?
                        """,
                        (new_price, new_qty, veg[0]))

                        conn.commit()

                        st.session_state["edit_id"] = None

                        st.success("Updated Successfully")

                        st.rerun()

                with c2:

                    if st.button("Cancel", key=f"cancel{veg[0]}"):

                        st.session_state["edit_id"] = None

                        st.rerun()

    st.markdown("---")

    st.subheader("📊 Sales History")

    cursor.execute("""
        SELECT
            o.vegetable,
            o.quantity,
            o.order_date
        FROM orders o
        JOIN vegetables v
        ON o.vegetable=v.vegetable_name
        WHERE v.farmer_name=?
        ORDER BY o.order_date DESC
    """, (username,))

    sales = cursor.fetchall()

    if sales:

        for sale in sales:

            with st.container(border=True):

                st.write(f"🥬 {sale[0]}")
                st.write(f"📦 Sold : {sale[1]} Kg")
                st.write(f"📅 {sale[2]}")

    else:

        st.info("No Sales Yet")

    st.markdown("---")

    st.subheader("💰 Income Summary")

    cursor.execute("""
        SELECT
            SUM(o.quantity*v.price)
        FROM orders o
        JOIN vegetables v
        ON o.vegetable=v.vegetable_name
        WHERE v.farmer_name=?
    """, (username,))

    income = cursor.fetchone()[0]

    if income is None:
        income = 0

    cursor.execute("""
        SELECT COUNT(*)
        FROM orders o
        JOIN vegetables v
        ON o.vegetable=v.vegetable_name
        WHERE v.farmer_name=?
    """, (username,))

    total_orders = cursor.fetchone()[0]

    cursor.execute("""
        SELECT
            vegetable,
            SUM(quantity) AS sold
        FROM orders
        GROUP BY vegetable
        ORDER BY sold DESC
        LIMIT 1
    """)

    best = cursor.fetchone()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("💰 Total Income", f"₹{income:.2f}")

    with col2:
        st.metric("📦 Orders", total_orders)

    with col3:

        if best:
            st.metric("🥇 Best Seller", best[0])
        else:
            st.metric("🥇 Best Seller", "-")