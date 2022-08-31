import psycopg2


def insert_response(connection, image_name, bucket, id, response):
    try:
        cursor = connection.cursor()

        postgres_insert_query = """INSERT INTO kagameshi_responses (image_name, bucket, user_id, response) VALUES (%s,%s,%s,%s)"""
        record_to_insert = (image_name, bucket, id, response)
        cursor.execute(postgres_insert_query, record_to_insert)

        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record", error)


def create_table_if_not_exist(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS kagameshi_responses (image_name VARCHAR NOT NULL, bucket VARCHAR "
                       "NOT NULL, user_id VARCHAR NOT NULL, response VARCHAR NOT NULL);")

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
