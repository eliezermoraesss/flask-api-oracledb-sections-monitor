from flask import Flask, render_template, redirect, url_for, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from db import run_query, execute_command, get_connection

app = Flask(__name__)

QUERY = """
select 'ALTER SYSTEM KILL SESSION '|| ''''||s.sid||','||s.serial#||'''' ||' IMMEDIATE' AS KILL, 
       s.sql_address,
       s.inst_id,
       s.sid,
       s.serial#,
       s.username,
       p.spid,
       s.osuser,
       s.EVENT,
       trunc(s.last_call_et/3600) horas,
       trunc(s.last_call_et/60) minutos,
       s.machine,
       s.client_info,
       s.program,
       to_char(s.LOGON_TIME,'dd/mm/yyyy hh24:mi:ss') LOGON_TIME,
       sysdate HORA_ATUAL,
       s.PREV_SQL_ADDR,
       s.paddr,
       s.taddr,
       s.machine
from gv$session s, gv$process p
WHERE s.paddr = p.addr
     and s.inst_id = p.inst_id
     and s.status='ACTIVE'
     and s.username is not null
     and TYPE<> 'BACKGROUND'
order by TYPE, logon_time
"""

# Armazena o último resultado da query (cache em memória)
last_result = {"cols": [], "rows": []}


def monitor_sessions():
    """Executa a query e atualiza o cache global."""
    global last_result
    cols, rows = run_query(QUERY)
    last_result = {"cols": cols, "rows": rows}

    # Auto kill se >= 20 sessões ativas
    if len(rows) >= 20:
        kill_index = cols.index("KILL")
        for r in rows:
            cmd = r[kill_index].strip().rstrip(";")  # remove ; e espaços extras
            execute_command(cmd)


# Scheduler em background para monitorar automaticamente
scheduler = BackgroundScheduler()
scheduler.add_job(monitor_sessions, "interval", seconds=1)  # a cada 3s
scheduler.start()


@app.route("/")
def index():
    return render_template("index.html", data=last_result)


@app.route("/kill_all")
def kill_all():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT SID, SERIAL#, USERNAME FROM V$SESSION
        WHERE USERNAME IS NOT NULL AND USERNAME != 'SYSTEM'
    """)
    for sid, serial, user in cursor.fetchall():
        cursor.execute(f"ALTER SYSTEM KILL SESSION '{sid},{serial}'immediate")
    connection.commit()
    return redirect(url_for("index"))


@app.route("/kill/<sid>/<serial>")
def kill_session(sid, serial):
    username = request.args.get("username", "").upper()

    if username == "SYSTEM":
        return jsonify({"error": "Sessão SYSTEM é protegida e não pode ser encerrada."}), 403

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(f"ALTER SYSTEM KILL SESSION '{sid},{serial}' IMMEDIATE")
        connection.commit()
        return redirect(url_for("index"))
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
