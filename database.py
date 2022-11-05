import psycopg2

def sql_execute(query, data=[]):
    conn = psycopg2.connect("dbname=pokemon_favourites")
    cur = conn.cursor()
    if "SELECT" in query:
        cur.execute(query, data)
        db_data = cur.fetchall()
        
        return db_data
    elif "INSERT" in query or "DELETE" in query or "UPDATE" in query:
        cur.execute(query, data)
        conn.commit()
        return

    cur.close()
    conn.close()