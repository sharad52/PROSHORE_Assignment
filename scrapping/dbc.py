import psycopg2


def connectToDB():
    conn = psycopg2.connect(
        host='localhost',
        database='proshore',
        user='proshore',
        password='proshore'
    )

    return conn


def insertData(job, tableName):

    conn = connectToDB()
    cur = conn.cursor()

    insertSQL = f"""
        insert into public.content(title, description, blog_image_url, author_name, author_image_url, author_designation, reading_time)
        values('{job[0]}', '{job[1]}', '{job[2]}', '{job[3]}', '{job[4]}', '{job[5]}', '{job[6]}')
    """

    cur.execute(insertSQL)
    conn.commit()
    cur.close()
    conn.close()


def truncateTable(tableName):
    conn = connectToDB()
    cur = conn.cursor()

    truncateSQL = f"""
        truncate table {tableName}
    """

    cur.execute(truncateSQL)
    conn.commit()
    cur.close()
    conn.close()
