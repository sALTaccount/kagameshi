import psycopg2


def insert_response(connection, image_id, user_id, response):
    try:
        cursor = connection.cursor()

        postgres_insert_query = """INSERT INTO kagameshi_responses (image_id, user_id, response) VALUES (%d,%d,%s)"""
        record_to_insert = (image_id, user_id, response)
        cursor.execute(postgres_insert_query, record_to_insert)

        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record", error)


def create_table_if_not_exist(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS kagameshi_responses (image_id BIGINT NOT NULL,"
                       "user_id BIGINT NOT NULL, response VARCHAR NOT NULL);")

        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Failed to create table", error)

def get_responses(connection):
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM kagameshi_responses;""")
    responses = cursor.fetchall()
    if len(responses) == 0:
        return None
    return responses

def get_response(connection, post_id):
    cursor = connection.cursor()
    cursor.execute("""SELECT * from kagameshi_responses WHERE image_id = %s""", (post_id,))
    res = cursor.fetchall()
    if not len(res):
        return None
    return res
