'''model for all CRUD  operations in postgre sql'''
import os
import psycopg2
import psycopg2.extras
from werkzeug.security import check_password_hash

# Database url

URL = "dbname='andelaapiv2' host='localhost'\
             port='5432' user='postgres' password='password'"

DATABASE_URL = os.getenv('DATABASE_URL', URL)


class Model():
    '''class to perform all CRUD methods'''

    def connect(self):
        '''make a connection to postgre sql using psycopg2'''
        connect = psycopg2.connect(DATABASE_URL)
        return connect

    def create_tables(self):
        """Create 'users' and 'incidents' tables
        in database if they do not already exist"""
        con = self.connect()
        cursor = con.cursor()
        queries = self.tables()
        for query in queries:
            cursor.execute(query)
        cursor.close()
        con.commit()
        con.close()

    def tables(self):
        users = """CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            firstname VARCHAR(25) NOT NULL,
            lastname VARCHAR(25) NOT NULL,
            othername VARCHAR(25),
            email VARCHAR(50) UNIQUE NOT NULL,
            phoneNumber VARCHAR(25),
            username VARCHAR(25) UNIQUE NOT NULL,
            pw_hash VARCHAR(250) UNIQUE NOT NULL,
            registered VARCHAR(200) default current_timestamp,
            isAdmin BOOLEAN DEFAULT 'False' NOT NULL )"""
        incidents = """CREATE TABLE IF NOT EXISTS incidents (
            id SERIAL PRIMARY KEY,
            createdOn VARCHAR(100) default current_timestamp,
            createdBy VARCHAR DEFAULT 'Lebron',
            type VARCHAR NOT NULL,
            location VARCHAR,
            status VARCHAR DEFAULT 'draft',
            Images VARCHAR,
            Videos VARCHAR,
            comment VARCHAR(500) NOT NULL )"""
        tables_query = [users, incidents]
        return tables_query

    def drop_tables(self):
        """Drop 'users' and 'incidents' tables from database"""
        con = self.connect()
        cursor = con.cursor()
        cursor.execute("""DROP TABLE IF EXISTS users,incidents CASCADE""")
        cursor.close()
        con.commit()
        con.close()

    def update_intervention_status(self, patched):
        """Edit the 'status' field of an intervention record"""
        con = self.connect()
        cursor = con.cursor()
        sql = """UPDATE incidents
                    SET status = %s
                    WHERE id = %s AND type = 'Intervention'"""
        cursor.execute(sql, patched)
        cursor.close()
        con.commit()
        con.close()

    def update_redflag_status(self, patched):
        """Edit the 'status' field of an intervention record"""
        con = self.connect()
        cursor = con.cursor()
        sql = """UPDATE incidents
                    SET status = %s
                    WHERE id = %s AND type = 'Redflag'"""
        cursor.execute(sql, patched)
        cursor.close()
        con.commit()
        con.close()

    def get_specific_intervention_record(self, intervention_id):
        """get a specific intervention record"""
        con = self.connect()
        cursor = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        sql = """SELECT * FROM incidents WHERE id = %s"""
        cursor.execute(sql, (intervention_id,))
        record = cursor.fetchone()
        cursor.close()
        con.commit()
        con.close()
        return record

    def create_intervention_record(self, posted):
        """add an  intervention record"""
        con = self.connect()
        cursor = con.cursor()
        sql = """INSERT INTO incidents(type,location,Images,
                 Videos,comment,createdBy)
                 VALUES( %s, %s, %s,
                 %s, %s,%s)"""
        cursor.execute(sql, posted)
        cursor.close()
        con.commit()
        con.close()

    def fetch_recent_id(self):
        """get latest incident record id"""
        con = self.connect()
        cursor = con.cursor()
        cursor.execute("SELECT id FROM incidents ORDER BY id DESC")
        record = cursor.fetchone()
        cursor.close()
        con.commit()
        con.close()
        return record

    def check_current_user(self, check_user):
        """check if this is the current user"""
        con = self.connect()
        cursor = con.cursor()
        sql = """SELECT * FROM incidents WHERE id = %s AND \
              createdBy = %s"""
        cursor.execute(sql, check_user)
        record = cursor.fetchone()
        if record is None or record is "":
            return False
        cursor.close()
        con.commit()
        con.close()
        return True

    def check_current_user_all_incidents(self, current_user):
        """check if this is the current user"""
        con = self.connect()
        cursor = con.cursor()
        sql = """SELECT * FROM incidents WHERE createdBy = %s"""
        cursor.execute(sql, (current_user,))
        record = cursor.fetchone()
        if record is None or record is "":
            return False
        cursor.close()
        con.commit()
        con.close()
        return True

    def get_all_interventions_records(self, current_user):
        """get all intervention records for login users """
        con = self.connect()
        cursor = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        sql = "SELECT * FROM incidents WHERE createdBy = %s"
        cursor.execute(sql, (current_user,))
        get_list = (cursor.fetchall())
        cursor.close()
        con.commit()
        con.close()
        return get_list

    def save_user_details(self, posted):
        """add a new user to the  database"""
        con = self.connect()
        cursor = con.cursor()
        sql = """INSERT INTO users(firstname, lastname, othername, email,
                 phoneNumber, username, pw_hash,isAdmin) VALUES(%s, %s, %s, %s,
                 %s, %s, %s, %s)"""
        cursor.execute(sql, posted)
        cursor.close()
        con.commit()
        con.close()

    def update_intervention_location(self, patched):
        """patch the location of a  specific record"""
        con = self.connect()
        cursor = con.cursor()
        sql = """UPDATE incidents
                    SET location = %s
                    WHERE id = %s"""
        cursor.execute(sql, patched)
        cursor.close()
        con.commit()
        con.close()

    def update_intervention_comment(self, patched):
        """patch the comment of a specific record"""
        con = self.connect()
        cursor = con.cursor()
        sql = """UPDATE incidents
                    SET comment = %s
                    WHERE id = %s"""
        cursor.execute(sql, patched)
        cursor.close()
        con.commit()
        con.close()

    def delete_specific_record(self, intervention_id):
        """Delete a specific intervention record"""
        con = self.connect()
        cursor = con.cursor()
        cursor.execute("DELETE FROM incidents WHERE id = %s",
                       (intervention_id,))
        cursor.close()
        con.commit()
        con.close()

    def commit(self):
        """
        commit changes to the db
        """
        con = self.connect()
        con.commit()

    def close(self):
        """
            close the cursor and the connection
        """
        con = self.connect()
        cursor = con.cursor()
        cursor.close()

    def findOne(self, intervention_id):
        """ return one item from query"""
        con = self.connect()
        cursor = con.cursor()
        sql = """SELECT * FROM incidents WHERE id = %s"""
        cursor.execute(sql, (intervention_id,))
        record = cursor.fetchone()
        return record

    def findAll(self):
        """ return all items from query"""
        con = self.connect()
        cursor = con.cursor()
        return self.cursor.fetchall()

    def validate_user_details(self, username, email):
        """method to sign up a user"""
        con = self.connect()
        cursor = con.cursor()
        cursor.execute("SELECT username FROM users\
                         WHERE username = %s", (username,))
        user = cursor.fetchone()
        if user is not None:
            return False

        cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
        mail = cursor.fetchone()
        cursor.close()
        con.commit()
        con.close()
        if mail is not None:
            return False
        return True

    def login_user(self, username, password):
        """method to login a user."""
        con = self.connect()
        cursor = con.cursor()
        cursor.execute("SELECT username,pw_hash \
                        FROM users WHERE username = %s", (username,))
        logincredentials = cursor.fetchone()
        cursor.close()
        con.commit()
        con.close()

        if logincredentials is None:
            return False
        if username != logincredentials[0]:
            return False
        if not check_password_hash(logincredentials[1], password):
            return False
        return True

    def check_isadmin(self, current_user):
        """checks if is Admin"""
        con = self.connect()
        cursor = con.cursor()
        sql = """SELECT * FROM users WHERE username = %s AND \
              isAdmin = TRUE"""
        cursor.execute(sql, (current_user,))
        record = cursor.fetchone()
        if record is None or record is "":
            return False
        cursor.close()
        con.commit()
        con.close()
        return True

    def list_users(self):
        """lists usera in  descending id order"""
        con = self.connect()
        cursor = con.cursor()
        cursor.execute("SELECT id FROM users ORDER BY id DESC")
        record = cursor.fetchone()
        cursor.close()
        con.commit()
        con.close()
        return record

    def get_all_users(self):
        """Fetch all users"""
        con = self.connect()
        cursor = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("SELECT * FROM users")
        get_list = (cursor.fetchall())
        cursor.close()
        con.commit()
        con.close()
        return get_list

    def get_all_incindents(self):
        """Fetch all incidents"""
        con = self.connect()
        cursor = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("SELECT * FROM incidents")
        get_list = (cursor.fetchall())
        cursor.close()
        con.commit()
        con.close()
        return get_list
