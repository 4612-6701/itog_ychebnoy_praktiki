import psycopg
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def registration(username, password, role):
    hashed_password = hash_password(password)
    with psycopg.connect(
        dbname='login_final',
        user='postgres',
        password='Admin',
        host='localhost',
        port=5432,
        connect_timeout=5
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO public.registration (username, password, role) VALUES (%s, %s, %s)
        """,(username,hashed_password, role)
        )
def check_user(username, password):
    hashed_password = hash_password(password)
    with psycopg.connect(
        dbname='login_final',
        user='postgres',
        password='Admin',
        host='localhost',
        port=5432,
        connect_timeout=5
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT role FROM public.registration WHERE username = %s AND password = %s""", 
                           (username, hashed_password)
                           )
            result = cursor.fetchone()
        # return result is not None
        if result:
            return result[0]
        return None