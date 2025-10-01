import oracledb as cx_Oracle

def get_connection():
    # ajuste para suas credenciais
    dsn = cx_Oracle.makedsn("MULTFER.DDNS.ME", 1521, service_name="PROD")
    return cx_Oracle.connect(user="system", password="oracle19c", dsn=dsn)

def run_query(query):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query)
    cols = [col[0] for col in cur.description]
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return cols, rows

def execute_command(command):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(command)
    conn.commit()
    cur.close()
    conn.close()
