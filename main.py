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

def load_table_data(conn):
    # Get a cursor to execute SQL queries
    cursor = conn.cursor()
    
    # Call the get_all_employees function in the database and get column headers
    rows, description = call_get_all_employees(cursor)

    # Get the current Calc document
    ctx = uno.getComponentContext()
    smgr = ctx.ServiceManager
    desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
    model = desktop.getCurrentComponent()
    sheet = model.CurrentController.ActiveSheet
    
    oSelection = model.getCurrentSelection()
    oArea = oSelection.getRangeAddress()
    currentRow = oArea.StartRow
    currentCol = oArea.StartColumn

    # Set column headers from the database
    headers = [col[0] for col in description]  # Extract column names from cursor.description
    for j, header in enumerate(headers):
        sheet.getCellByPosition(currentCol + j, currentRow).setString(header)

    # Populate the Calc sheet with data from the database
    for i, row in enumerate(rows):
        for j, value in enumerate(row):
            sheet.getCellByPosition(currentCol + j, currentRow + i + 1).setString(str(value))

def main():
    # Main function to execute the data loading process
    conn = connect_to_db()  # Establish connection to the database
    load_table_data(conn)
    conn.close()            # Close the database connection
    
def clear_sheet():
    # Get the current Calc document and sheet
    ctx = uno.getComponentContext()
    smgr = ctx.ServiceManager
    desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
    model = desktop.getCurrentComponent()
    sheet = model.Sheets.getByIndex(0)

    # Clear the entire sheet by setting the value of all cells to an empty string
    cursor = sheet.createCursor()
    cursor.gotoEndOfUsedArea(False)  # Move to the last used cell in the sheet
    last_row = cursor.RangeAddress.EndRow
    last_col = cursor.RangeAddress.EndColumn
    
    # Iterate over all cells in the used area and clear them
    for row in range(last_row + 1):
        for col in range(last_col + 1):
            sheet.getCellByPosition(col, row).setString("")


if __name__ == "__main__":
    main()
