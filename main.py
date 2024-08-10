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
    return cursor.fetchall()

def load_table_data(conn):
    # Get a cursor to execute SQL queries
    cursor = conn.cursor()
    
    # Call the get_all_employees function in the database
    rows = call_get_all_employees(cursor)

    # Get the current Calc document
    ctx = uno.getComponentContext()
    smgr = ctx.ServiceManager
    desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
    model = desktop.getCurrentComponent()
    sheet = model.Sheets.getByIndex(0)

    # Populate the Calc sheet with data from the database
    for i, row in enumerate(rows):
        for j, value in enumerate(row):
            sheet.getCellByPosition(j, i).setString(str(value))

def main():
    # Main function to execute the data loading process
    conn = connect_to_db()  # Establish connection to the database
    load_table_data(conn)   # Load data and write it to the Calc sheet
    conn.close()            # Close the database connection

if __name__ == "__main__":
    main()
