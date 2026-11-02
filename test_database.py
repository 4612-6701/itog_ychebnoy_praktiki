import psycopg

def save_test_result(username, score, grade):
    with psycopg.connect(
        dbname='data_final',
        user='postgres',
        password='Admin',
        host='localhost',
        port=5432,
        connect_timeout=5
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute('''
                INSERT INTO public.test_results (username, score, grade) VALUES (%s, %s, %s)
            ''',(username,score, grade)
            )
def get_all_results():
    with psycopg.connect(
        dbname='data_final',
        user='postgres',
        password='Admin',
        host='localhost',
        port=5432,
        connect_timeout=5
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT username, score, grade FROM public.test_results ORDER BY id DESC
            '''
            )
            return cursor.fetchall()
