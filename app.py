from flask import Flask, render_template, redirect, url_for
from apscheduler.schedulers.background import BackgroundScheduler
from db import run_query, execute_command

app = Flask(__name__)

QUERY = """
select 'ALTER SYSTEM KILL SESSION '|| ''''||s.sid||','||s.serial#||'''' ||' immediate;' AS KILL, 
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
order by TYPE,logon_time
"""

last_result = {"cols": [], "rows": []}

def monitor_sessions():
    global last_result
    cols, rows = run_query(QUERY)
    last_result = {"cols": cols, "rows": rows}

    # Auto kill se >= 20
    if len(rows) >= 20:
        kill_index = cols.index("KILL")
        for r in rows:
            execute_command(r[kill_index])

scheduler = BackgroundScheduler()
scheduler.add_job(monitor_sessions, "interval", seconds=1)
scheduler.start()

@app.route("/")
def index():
    return render_template("index.html", data=last_result)

@app.route("/kill_all")
def kill_all():
    if last_result["rows"]:
        kill_index = last_result["cols"].index("KILL")
        for r in last_result["rows"]:
            execute_command(r[kill_index])
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
