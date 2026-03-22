import sqlite3

conn = sqlite3.connect('pulse.db')
conn.row_factory = sqlite3.Row
rows = conn.execute(
    """SELECT colour_name, hex, confidence, recorded_at, lang
       FROM colour_forecasts
       WHERE lang = 'en'
       ORDER BY recorded_at ASC"""
).fetchall()
for r in rows:
    print(r['recorded_at'], r['colour_name'], r['hex'])
conn.close()