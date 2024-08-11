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

def get_model():
    ctx = uno.getComponentContext()
    smgr = ctx.ServiceManager
    desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
    model = desktop.getCurrentComponent()
    return model

def call_get_all_employees(conn):
    # Call the PostgreSQL function 'get_all_employees'
    cursor = conn.cursor()
    function_name = 'get_all_employees'
    cursor.callproc(function_name)
    return cursor.fetchall(), cursor.description

def call_get_all_employees_between_codes(conn, params):
    # Call the PostgreSQL function 'get_all_employees_between_codes'
    cursor = conn.cursor()
    function_name = 'get_employees_between_codes'
    
    cursor.callproc(function_name, params)
    return cursor.fetchall(), cursor.description

def load_table_data(rows, description):
    model = get_model()
    sheet = model.CurrentController.ActiveSheet 
    
    oSelection = model.getCurrentSelection()
    oArea = oSelection.getRangeAddress()
    currentRow = oArea.StartRow
    currentCol = oArea.StartColumn

    # Set column headers from the database
    headers = [col[0] for col in description]
    for j, header in enumerate(headers):
        sheet.getCellByPosition(currentCol + j, currentRow).setString(header)

    # Populate the Calc sheet with data from the database
    for i, row in enumerate(rows):
        for j, value in enumerate(row):
            sheet.getCellByPosition(currentCol + j, currentRow + i + 1).setString(str(value))

def macros_1():
    conn = connect_to_db()  
    rows, description = call_get_all_employees(conn)
    load_table_data(rows, description)
    conn.close()
    
def macros_2():
    conn = connect_to_db()  
    model = get_model()
    sheet = model.CurrentController.ActiveSheet
    
    min_code = int(sheet.getCellRangeByName("D1").getValue())
    max_code = int(sheet.getCellRangeByName("D2").getValue())

    rows, description = call_get_all_employees_between_codes(conn, (min_code, max_code))
    load_table_data(rows, description)
    conn.close()
    
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
    macros_1()
