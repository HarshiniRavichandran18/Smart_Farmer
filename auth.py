import streamlit as st
import sqlite3


def login(conn, cursor, T):
    """
    Returns:
        (username, role) if login successful
        (None, None) otherwise
    """

    st.title("🔐 Smart Farmer Login")

    username = st.text_input(T["username"]).strip().lower()

    password = st.text_input(
        T["password"],
        type="password"
    )

    role_ui = st.selectbox(
        T["role"],
        [T["farmer"], T["customer"]]
    )

    role = "Farmer" if role_ui == T["farmer"] else "Customer"

    col1, col2 = st.columns(2)

    # ---------------- LOGIN ----------------
    with col1:

        if st.button(T["login"], use_container_width=True):

            cursor.execute("""
                SELECT *
                FROM users
                WHERE username=?
                AND password=?
                AND role=?
            """, (username, password, role))

            user = cursor.fetchone()

            if user:

                st.success("Login Successful!")

                return username, role

            else:

                st.error("Invalid Username or Password.")

    # ---------------- REGISTER ----------------
    with col2:

        if st.button("Register", use_container_width=True):

            if username == "" or password == "":

                st.warning("Enter Username and Password.")

            else:

                try:

                    cursor.execute("""
                        INSERT INTO users
                        (
                            username,
                            password,
                            role
                        )
                        VALUES
                        (?,?,?)
                    """, (username, password, role))

                    conn.commit()

                    st.success("Registration Successful!")

                except sqlite3.IntegrityError:

                    st.warning("Username already exists.")


    return None, None


# ---------------- LOGOUT ----------------

def logout():

    st.session_state.user = None
    st.session_state.role = None

    if "cart" in st.session_state:
        st.session_state.cart = []

    st.rerun()