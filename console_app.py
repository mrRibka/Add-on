import psycopg2

def get_all_functions():
    try:
        connection = psycopg2.connect(
            dbname="mydatabase",
            user="postgres",
            password="root",
            host="localhost",
            port="5432"
        )
        
        cursor = connection.cursor()
        
        cursor.execute("""
            SELECT routine_name 
            FROM information_schema.routines 
            WHERE routine_type='FUNCTION' 
            AND specific_schema='public';
        """)
        
        functions = cursor.fetchall()
        
        return [func[0] for func in functions]
    
    except (Exception, psycopg2.Error) as error:
        print("?????? ??? ??????????? ? PostgreSQL", error)
        return []
    
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("?????????? ? PostgreSQL ???????")

def get_function_parameters(function_name):
    try:
        connection = psycopg2.connect(
            dbname="mydatabase",
            user="postgres",
            password="root",
            host="localhost",
            port="5432"
        )
        
        cursor = connection.cursor()

        query = """
        SELECT
            p.proname,
            pg_catalog.pg_get_function_result(p.oid) AS result_type,
            pg_catalog.pg_get_function_arguments(p.oid) AS arguments
        FROM pg_catalog.pg_proc p
            LEFT JOIN pg_catalog.pg_namespace n ON n.oid = p.pronamespace
        WHERE p.proname = %s;
        """
        
        cursor.execute(query, (function_name,))

        functions = cursor.fetchall()
        
        if not functions:
            print("??????? ?? ???????")
            return []

        result = []
        for function in functions:
            proname, result_type, arguments = function
            args = []
            if arguments:
                args = arguments.split(", ")
                args = [(arg.split(" ")[0], arg.split(" ")[1]) for arg in args]
            result.append((proname, result_type, args))
            
        print(result)
        return result
    
    except (Exception, psycopg2.Error) as error:
        print("?????? ??? ??????????? ? PostgreSQL", error)
        return []
    
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("?????????? ? PostgreSQL ???????")

def call_function(function_name, params):
    try:
        connection = psycopg2.connect(
            dbname="mydatabase",
            user="postgres",
            password="root",
            host="localhost",
            port="5432"
        )
        
        cursor = connection.cursor()
        
        cursor.callproc(function_name, params)
        
        rows = cursor.fetchall()
        
        return rows
    
    except (Exception, psycopg2.Error) as error:
        print("?????? ??? ??????????? ? PostgreSQL", error)
        return None
    
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("?????????? ? PostgreSQL ???????")


functions = get_all_functions()
if not functions:
    print("??? ????????? ???????.")
else:
    print("????????? ???????:")
    for idx, func in enumerate(functions, start=1):
        print(f"{idx}. {func}")

    selected_idx = int(input("???????? ????? ??????? ??? ??????: "))
    if selected_idx < 1 or selected_idx > len(functions):
        print("???????? ????? ???????.")
    else:
        selected_function = functions[selected_idx - 1]
        parameters = get_function_parameters(selected_function)
        params = []
        for param in parameters:
            param_name = param[0]
            param_type = param[1]
            if param_type == 'integer':
                params.append(int(input(f"??????? ???????? ??? {param_name} ({param_type}): ")))
            elif param_type == 'character varying' or param_type == 'text':
                params.append(input(f"??????? ???????? ??? {param_name} ({param_type}): "))
            elif param_type == 'date':
                params.append(input(f"??????? ???????? ??? {param_name} ({param_type}, YYYY-MM-DD): "))
            elif param_type == 'boolean':
                val = input(f"??????? ???????? ??? {param_name} ({param_type}, true/false): ").lower()
                params.append(True if val == 'true' else False)
            elif param_type == 'numeric':
                params.append(float(input(f"??????? ???????? ??? {param_name} ({param_type}): ")))

        result = call_function(selected_function, params)
        
        if result is not None:
            print("?????????? ?????????? ???????:")
            for row in result:
                print(row)
        else:
            print("?? ??????? ????????? ???????.")
