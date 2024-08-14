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
    desktop = XSCRIPTCONTEXT.getDesktop()
    model = desktop.getCurrentComponent()
    return model

def call_get_all_employees(conn):
    # Call the PostgreSQL function 'get_all_employees'
    cursor = conn.cursor()
    function_name = 'get_all_employees'
    cursor.callproc(function_name)
    return cursor.fetchall(), cursor.description

def call_create_employee(conn, params):
    # Call the PostgreSQL function 'create_employee'
    cursor = conn.cursor()
    function_name = 'create_employee'
    cursor.callproc(function_name, params)
    return cursor.fetchall(), cursor.description

def call_update_employee(conn, params):
    # Call the PostgreSQL function 'update_employee'
    cursor = conn.cursor()
    function_name = 'update_employee'
    cursor.callproc(function_name, params)
    return cursor.fetchall(), cursor.description

def call_delete_employee_by_id(conn, params):
    # Call the PostgreSQL function 'delete_employee_by_id'
    cursor = conn.cursor()
    function_name = 'delete_employee_by_id'
    cursor.callproc(function_name, params)
    return cursor.fetchall(), cursor.description

def call_get_employees_between_codes(conn, params):
    # Call the PostgreSQL function 'get_employees_between_codes'
    cursor = conn.cursor()
    function_name = 'get_employees_between_codes'
    cursor.callproc(function_name, params)
    return cursor.fetchall(), cursor.description

def load_table_data(rows, description):
    model = get_model()
    sheet = model.CurrentController.ActiveSheet
    
    oSelection = model.getCurrentSelection()
    oArea = oSelection.getRangeAddress()
    #startRow = oArea.StartRow
    #startCol = oArea.StartColumn
    startRow = 2
    startCol = 0

    # Set column headers from the database
    headers = [col[0] for col in description]
    for j, header in enumerate(headers):
        sheet.getCellByPosition(startCol + j, startRow).setString(header)

    # Populate the Calc sheet with data from the database
    for i, row in enumerate(rows):
        for j, value in enumerate(row):
            sheet.getCellByPosition(startCol + j, startRow + i + 1).setString(str(value))

def macros_1():
    conn = connect_to_db()  
    rows, description = call_get_all_employees(conn)
    load_table_data(rows, description)
    conn.close()
    
def macros_2():
    conn = connect_to_db()  
    model = get_model()
    #sheet = doc.getCurrentController().getActiveSheet()
    sheet = model.CurrentController.ActiveSheet
    
    min_code = sheet.getCellRangeByName("D1").getString()
    max_code = sheet.getCellRangeByName("D2").getString()

    rows, description = call_get_employees_between_codes(conn, (min_code, max_code))
    load_table_data(rows, description)
    conn.close()
    
def clear_sheet():
    model = get_model()
    sheet = model.Sheets.getByIndex(0)

    cursor = sheet.createCursor()
    cursor.gotoEndOfUsedArea(False)  # Move to the last used cell in the sheet
    last_row = cursor.RangeAddress.EndRow
    last_col = cursor.RangeAddress.EndColumn
    
    # Iterate over all cells in the used area and clear them
    for row in range(last_row + 1):
        for col in range(last_col + 1):
            sheet.getCellByPosition(col, row).setString("")

