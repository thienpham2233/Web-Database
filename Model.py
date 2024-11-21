import psycopg2
from psycopg2 import sql

class DatabaseModel:
    def __init__(self, db_name, user, password, host, port):
        try:
            self.conn = psycopg2.connect(
                dbname=db_name,
                user=user,
                password=password,
                host=host,
                port=port
            )
            self.cur = self.conn.cursor()
        except Exception as e:
            raise Exception(f"Error connecting to the database: {e}")

    def load_data(self, table_name):
        try:
            query = sql.SQL("SELECT hoten, diachi, mssv FROM {}").format(sql.Identifier(table_name))
            self.cur.execute(query)
            return self.cur.fetchall()
        except Exception as e:
            raise Exception(f"Error loading data: {e}")


    def insert_data(self, table_name, column1, column2, column3):
        try:
            insert_query = sql.SQL("INSERT INTO {} (hoten, diachi, mssv) VALUES (%s, %s, %s)").format(sql.Identifier(table_name))
            self.cur.execute(insert_query, (column1, column2, column3))
            self.conn.commit()
        except Exception as e:
            raise Exception(f"Error inserting data: {e}")

    def close_connection(self):
        try:
            if self.cur and not self.cur.closed:
                self.cur.close()
            if self.conn:
                self.conn.close()
        except Exception as e:
            raise Exception(f"Error closing the connection: {e}")
        
    def delete_data(self, selected_rows):
        for row_id in selected_rows:
            query = "DELETE FROM your_table_name WHERE id = %s"
            self.cursor.execute(query, (row_id,))
        self.connection.commit()
