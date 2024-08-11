import uno
import psycopg2

def connect_to_db():
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        dbname="mydatabase", 
        user="postgres", 
        password="root", 
        host="localhost", 
        port="5432"
    )
    return conn

def call_get_all_employees(cursor):
    # Call the PostgreSQL function 'get_all_employees' using cursor.callproc
    function_name = 'get_all_employees'
    params = ()
    cursor.callproc(function_name, params)
    return cursor.fetchall(), cursor.description

def load_table_data(conn, start_row=1, start_col=0):
    # Get a cursor to execute SQL queries
    cursor = conn.cursor()
    
    # Call the get_all_employees function in the database and get column headers
    rows, description = call_get_all_employees(cursor)

    # Get the current Calc document
    ctx = uno.getComponentContext()
    smgr = ctx.ServiceManager
    desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
    model = desktop.getCurrentComponent()
    sheet = model.Sheets.getByIndex(0)

    # Set column headers from the database
    headers = [col[0] for col in description]  # Extract column names from cursor.description
    for j, header in enumerate(headers):
        sheet.getCellByPosition(start_col + j, start_row).setString(header)

    # Populate the Calc sheet with data from the database
    for i, row in enumerate(rows):
        for j, value in enumerate(row):
            sheet.getCellByPosition(start_col + j, start_row + i + 1).setString(str(value))

def main():
    # Main function to execute the data loading process
    conn = connect_to_db()  # Establish connection to the database
    load_table_data(conn, start_row=2, start_col=2)  # Specify the starting row and column
    conn.close()            # Close the database connection

if __name__ == "__main__":
    main()
