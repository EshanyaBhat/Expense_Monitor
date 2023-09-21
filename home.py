import streamlit as st
import mysql.connector
import pandas as pd
from datetime import datetime

# Create a function to establish a database connection
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="expensetracker"
        )
        return connection
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        return None
    

def monthly_summary():
    connection = connect_to_database()
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT YEAR(Date) AS Year, MONTH(Date) AS Month, Type, SUM(Amount) AS Total "
                "FROM records "
                "GROUP BY YEAR(Date), MONTH(Date), Type "
                "ORDER BY Year, Month, Type"
            )
            summary_data = cursor.fetchall()

            # Convert the year to integer to remove the comma
            for entry in summary_data:
                entry['Year'] = int(entry['Year'])

            st.header("Monthly Summary")
            if not summary_data:
                st.warning("No records found.")
            else:
                summary_df = pd.DataFrame(summary_data)
                st.dataframe(summary_df)
        except Exception as e:
            st.error(f"Error fetching monthly summary from the database: {e}")
        finally:
            cursor.close()
            connection.close()


# Create a function to add expense/income records to the database
def add_record_to_database(date, record_type, amount):
    connection = connect_to_database()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO records (Date, Type, Amount) VALUES (%s, %s, %s)",
                (date, record_type, amount)
            )
            connection.commit()
            st.success("Record added successfully!")
        except Exception as e:
            st.error(f"Error adding record to the database: {e}")
        finally:
            cursor.close()
            connection.close()

# Create a Streamlit app
def main():
     
    st.title("Expense Monitor")

    st.image("expense-categories.jpg", use_column_width=True)


    # Create login functionality (you can enhance this for user authentication)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        if username == "Eshanya" and password == "Nevergiveup@1234":
            st.session_state.logged_in = True
            st.success("Logged in as {}".format(username))
            st.write("Welcome to the Expense Tracker App!")
        else:
            st.error("Invalid credentials. Please try again.")
            st.session_state.logged_in = False

    # Check if the user is logged in before allowing access to add records
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.warning("Please log in to add or edit records.")
        return

    # Add Expense/Income Form
    st.header("Add Expense/Income")
    record_date = st.date_input("Date", datetime.today())
    record_type = st.selectbox("Type", ["Expense", "Income"])
    amount = st.number_input("Amount", min_value=0.01)

    if st.button("Add Record"):
        add_record_to_database(record_date, record_type, amount)

    # Filter Records
    st.header("Filter Records")
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    selected_type = st.selectbox("Select Type", ["All", "Expense", "Income"])

    connection = connect_to_database()
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            if selected_type == "All":
                cursor.execute("SELECT * FROM records WHERE Date >= %s AND Date <= %s", (start_date, end_date))
            else:
                cursor.execute("SELECT * FROM records WHERE Date >= %s AND Date <= %s AND Type = %s", (start_date, end_date, selected_type))
            filtered_data = cursor.fetchall()
            st.header("List of Expenses/Income")
            if not filtered_data:
                st.warning("No records found.")
            else:
                st.dataframe(pd.DataFrame(filtered_data))
        except Exception as e:
            st.error(f"Error fetching records from the database: {e}")
        finally:
            cursor.close()
            connection.close()

    # Add a button to show the monthly summary
    if st.button("Show Monthly Summary"):
        monthly_summary()

if __name__ == "__main__":
    main()
