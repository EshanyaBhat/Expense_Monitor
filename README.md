# Expense_Monitor

This app is an Expense Monitor built using Streamlit, a Python library for creating web applications. It allows users to track their expenses and income by entering financial records and provides features to filter and view the records.

Login Screen:
Users are prompted to enter a username and password.
If the correct credentials are entered, the user is considered logged in.

Main Application Screen after login:
Users can add new financial records by specifying the date, type (expense or income), and amount and clicking the "Add Record" button.

Filtering Records:
Users can filter their financial records based on date range and type.
They can select a start and end date and choose to view "All," "Expense," or "Income" records.
Clicking the "Filter" button displays the filtered records in a tabular format.

Monthly Summary:
Users can click the "Show Monthly Summary" button to view a summary of monthly expenses and income.
The app retrieves this data from the database and displays it in a table format.
