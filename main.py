import uno
import psycopg2

def connect_to_db():
    conn = psycopg2.connect(
        dbname="mydatabase", 
        user="postgres", 
        password="root", 
        host="localhost", 
        port="5432"
    )
    return conn

def load_table_data(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees')
    rows = cursor.fetchall()

    ctx = uno.getComponentContext()
    smgr = ctx.ServiceManager
    desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
    model = desktop.getCurrentComponent()
    sheet = model.Sheets.getByIndex(0)

    for i, row in enumerate(rows):
        for j, value in enumerate(row):
            sheet.getCellByPosition(j, i).setString(str(value))

def on_button_click(event=None):
    conn = connect_to_db()
    load_table_data(conn)
    conn.close()

def create_button():
    ctx = uno.getComponentContext()
    smgr = ctx.ServiceManager
    desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
    doc = desktop.getCurrentComponent()
    sheet = doc.Sheets[0]  

    draw_page = sheet.DrawPage

    if draw_page.Forms.getCount() == 0:
        form = smgr.createInstanceWithContext("com.sun.star.form.component.Form", ctx)
        draw_page.Forms.append(form)
    else:
        form = draw_page.Forms.getByIndex(0)

    button_model = smgr.createInstanceWithContext("com.sun.star.form.component.CommandButton", ctx)
    button_model.Label = "Load Data"
    button_model.Name = "MyButton"
    
    button_shape = smgr.createInstanceWithContext("com.sun.star.drawing.ControlShape", ctx)
    button_shape.Control = button_model
    button_shape.setSize(5000, 1000)  
    button_shape.setPosition(1000, 1000)  

    draw_page.add(button_shape)
    
    def button_actionPerformed(event):
        on_button_click(event)

    button_model.addActionListener(uno.createUnoListener(ButtonClickListener(), "com.sun.star.awt.XActionListener"))

class ButtonClickListener:
    def actionPerformed(self, event):
        on_button_click(event)

    def disposing(self, event):
        pass

if __name__ == "__main__":
    create_button()
