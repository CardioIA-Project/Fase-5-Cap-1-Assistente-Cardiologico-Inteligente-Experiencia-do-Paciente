import sqlite3

conn = sqlite3.connect("db/clinica.db")
conn.execute(
    "INSERT INTO sinais_vitais "
    "(paciente_id, pressao_sistolica, pressao_diastolica, frequencia_cardiaca, adesao_tratamento_pct) "
    "VALUES (1, 195, 110, 130, 40)"
)
conn.commit()
conn.close()
print("leitura inserida com sucesso")
