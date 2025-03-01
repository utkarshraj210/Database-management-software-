import sqlite3
import streamlit as st

class DatabaseManager:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                mobile_number TEXT NOT NULL,
                email TEXT NOT NULL
            )
        """)
        self.connection.commit()

    def add_contact(self, name, mobile_number, email):
        self.cursor.execute("""
            INSERT INTO contacts (name, mobile_number, email) VALUES (?, ?, ?)
        """, (name, mobile_number, email))
        self.connection.commit()

    def view_contacts(self):
        self.cursor.execute("SELECT * FROM contacts")
        return self.cursor.fetchall()

    def update_contact(self, contact_id, name=None, mobile_number=None, email=None):
        if name:
            self.cursor.execute("UPDATE contacts SET name = ? WHERE id = ?", (name, contact_id))
        if mobile_number:
            self.cursor.execute("UPDATE contacts SET mobile_number = ? WHERE id = ?", (mobile_number, contact_id))
        if email:
            self.cursor.execute("UPDATE contacts SET email = ? WHERE id = ?", (email, contact_id))
        self.connection.commit()

    def delete_contact(self, contact_id):
        self.cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
        self.connection.commit()

    def __del__(self):
        self.connection.close()

def main():
    db = DatabaseManager("contacts.db")

    st.title("Contact Management System")

    menu = ["Add Contact", "View Contacts", "Update Contact", "Delete Contact"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Contact":
        st.subheader("Add Contact")
        name = st.text_input("Name")
        mobile_number = st.text_input("Mobile Number")
        email = st.text_input("Email")
        if st.button("Add"):
            db.add_contact(name, mobile_number, email)
            st.success("Contact added successfully!")
            st.write(db.view_contacts())  # Display contacts to verify addition

    elif choice == "View Contacts":
        st.subheader("View Contacts")
        contacts = db.view_contacts()
        for contact in contacts:
            st.text(f"ID: {contact[0]}, Name: {contact[1]}, Mobile: {contact[2]}, Email: {contact[3]}")

    elif choice == "Update Contact":
        st.subheader("Update Contact")
        contact_id = st.number_input("Contact ID", min_value=1, step=1)
        name = st.text_input("New Name")
        mobile_number = st.text_input("New Mobile Number")
        email = st.text_input("New Email")
        if st.button("Update"):
            db.update_contact(contact_id, name, mobile_number, email)
            st.success("Contact updated successfully!")
            st.write(db.view_contacts())  # Display contacts to verify update

    elif choice == "Delete Contact":
        st.subheader("Delete Contact")
        contact_id = st.number_input("Contact ID", min_value=1, step=1)
        if st.button("Delete"):
            db.delete_contact(contact_id)
            st.success("Contact deleted successfully!")
            st.write(db.view_contacts())  # Display contacts to verify deletion

if __name__ == "__main__":
    main()
