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
        conn = self.connect()
        cursor_tables = conn.cursor()
        cursor_tables.execute(
            """DROP TABLE IF EXISTS users,incidents CASCADE""")
        cursor_tables.close()
        conn.commit()
        conn.close()

    def update_intervention_status(self, patched):
        """Edit the 'status' field of an intervention record"""
        con_update = self.connect()
        cursor_update = con_update.cursor()
        sql = """UPDATE incidents
                    SET status = %s
                    WHERE id = %s AND type = 'Intervention'"""
        cursor_update.execute(sql, patched)
        cursor_update.close()
        con_update.commit()
        con_update.close()

    def update_redflag_status(self, patched):
        """Edit the 'status' field of an intervention record"""
        con_redfalg = self.connect()
        cursor_redflag = con_redfalg.cursor()
        sql = """UPDATE incidents
                    SET status = %s
                    WHERE id = %s AND type = 'Redflag'"""
        cursor_redflag.execute(sql, patched)
        cursor_redflag.close()
        con_redfalg.commit()
        con_redfalg.close()

    def get_specific_intervention_record(self, intervention_id):
        """get a specific intervention record"""
        con_specific = self.connect()
        cursor_specific = con_specific.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)
        sql = """SELECT * FROM incidents WHERE id = %s"""
        cursor_specific.execute(sql, (intervention_id,))
        record = cursor_specific.fetchone()
        cursor_specific.close()
        con_specific.commit()
        con_specific.close()
        return record

    def create_intervention_record(self, posted):
        """add an  intervention record"""
        con_create = self.connect()
        cursor_create = con_create.cursor()
        sql = """INSERT INTO incidents(type,location,Images,
                 Videos,comment,createdBy)
                 VALUES( %s, %s, %s,
                 %s, %s,%s)"""
        cursor_create.execute(sql, posted)
        cursor_create.close()
        con_create.commit()
        con_create.close()

    def fetch_recent_id(self):
        """get latest incident record id"""
        con_recent = self.connect()
        cursor_recent = con_recent.cursor()
        cursor_recent.execute("SELECT id FROM incidents ORDER BY id DESC")
        record = cursor_recent.fetchone()
        cursor_recent.close()
        con_recent.commit()
        con_recent.close()
        return record

    def check_current_user(self, check_user):
        """check if this is the current user"""
        con_current = self.connect()
        cursor_current = con_current.cursor()
        sql = """SELECT * FROM incidents WHERE id = %s AND \
              createdBy = %s"""
        cursor_current.execute(sql, check_user)
        record = cursor_current.fetchone()
        if record is None or record is "":
            return False
        cursor_current.close()
        con_current.commit()
        con_current.close()
        return True

    def check_current_user_all_incidents(self, current_user):
        """check if this is the current user"""
        con_incidents = self.connect()
        cursor_incidents = con_incidents.cursor()
        sql = """SELECT * FROM incidents WHERE createdBy = %s"""
        cursor_incidents.execute(sql, (current_user,))
        record = cursor_incidents.fetchone()
        if record is None or record is "":
            return False
        cursor_incidents.close()
        con_incidents.commit()
        con_incidents.close()
        return True

    def get_all_interventions_records(self, current_user):
        """get all intervention records for login users """
        con_rec = self.connect()
        cursor_rec = con_rec.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)
        sql = "SELECT * FROM incidents WHERE createdBy = %s"
        cursor_rec.execute(sql, (current_user,))
        get_list = (cursor_rec.fetchall())
        cursor_rec.close()
        con_rec.commit()
        con_rec.close()
        return get_list

    def save_user_details(self, posted):
        """add a new user to the  database"""
        con_dtails = self.connect()
        cursor_details = con_dtails.cursor()
        sql = """INSERT INTO users(firstname, lastname, othername, email,
                 phoneNumber, username, pw_hash,isAdmin) VALUES(%s, %s, %s, %s,
                 %s, %s, %s, %s)"""
        cursor_details.execute(sql, posted)
        cursor_details.close()
        con_dtails.commit()
        con_dtails.close()

    def update_intervention_location(self, patched):
        """patch the location of a  specific record"""
        con_location = self.connect()
        cursor_location = con_location.cursor()
        sql = """UPDATE incidents
                    SET location = %s
                    WHERE id = %s"""
        cursor_location.execute(sql, patched)
        cursor_location.close()
        con_location.commit()
        con_location.close()

    def update_intervention_comment(self, patched):
        """patch the comment of a specific record"""
        con_comment = self.connect()
        cursor_comment = con_comment.cursor()
        sql = """UPDATE incidents
                    SET comment = %s
                    WHERE id = %s"""
        cursor_comment.execute(sql, patched)
        cursor_comment.close()
        con_comment.commit()
        con_comment.close()

    def delete_specific_record(self, intervention_id):
        """Delete a specific intervention record"""
        con_del = self.connect()
        cursor_del = con_del.cursor()
        cursor_del.execute("DELETE FROM incidents WHERE id = %s",
                           (intervention_id,))
        cursor_del.close()
        con_del.commit()
        con_del.close()

    def commit(self):
        """
        commit changes to the db
        """
        con_on = self.connect()
        con_on.commit()

    def close(self):
        """
            close the cursor and the connection
        """
        con_lo = self.connect()
        cursor_lo = con_lo.cursor()
        cursor_lo.close()

    def findOne(self, intervention_id):
        """ return one item from query"""
        con_ne = self.connect()
        cursor_ne = con_ne.cursor()
        sql = """SELECT * FROM incidents WHERE id = %s"""
        cursor_ne.execute(sql, (intervention_id,))
        record = cursor_ne.fetchone()
        return record

    def findAll(self):
        """ return all items from query"""
        con_f = self.connect()
        cursor_f = con_f.cursor()
        return self.cursor_f.fetchall()

    def validate_user_details(self, username, email):
        """method to sign up a user"""
        con_val = self.connect()
        cursor_val = con_val.cursor()
        cursor_val.execute("SELECT username FROM users\
                         WHERE username = %s", (username,))
        user = cursor_val.fetchone()
        if user is not None:
            return False

        cursor_val.execute(
            "SELECT email FROM users WHERE email = %s", (email,))
        mail = cursor_val.fetchone()
        cursor_val.close()
        con_val.commit()
        con_val.close()
        if mail is not None:
            return False
        return True

    def login_user(self, username, password):
        """method to login a user."""
        con_lo = self.connect()
        cursor_lo = con_lo.cursor()
        cursor_lo.execute("SELECT username,pw_hash \
                        FROM users WHERE username = %s", (username,))
        logincredentials = cursor_lo.fetchone()
        cursor_lo.close()
        con_lo.commit()
        con_lo.close()

        if logincredentials is None:
            return False
        if username != logincredentials[0]:
            return False
        if not check_password_hash(logincredentials[1], password):
            return False
        return True

    def check_isadmin(self, current_user):
        """checks if is Admin"""
        con_is = self.connect()
        cursor_is = con_is.cursor()
        sql = """SELECT * FROM users WHERE username = %s AND \
              isAdmin = TRUE"""
        cursor_is.execute(sql, (current_user,))
        record = cursor_is.fetchone()
        if record is None or record is "":
            return False
        cursor_is.close()
        con_is.commit()
        con_is.close()
        return True

    def list_users(self):
        """lists usera in  descending id order"""
        con_li = self.connect()
        cursor_li = con_li.cursor()
        cursor_li.execute("SELECT id FROM users ORDER BY id DESC")
        record = cursor_li.fetchone()
        cursor_li.close()
        con_li.commit()
        con_li.close()
        return record

    def get_all_users(self):
        """Fetch all users"""
        con_al = self.connect()
        cursor_al = con_al.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)
        cursor_al.execute("SELECT * FROM users")
        get_list = (cursor_al.fetchall())
        cursor_al.close()
        con_al.commit()
        con_al.close()
        return get_list

    def get_all_incindents(self):
        """Fetch all incidents"""
        con_gt = self.connect()
        cursor_gt = con_gt.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)
        cursor_gt.execute("SELECT * FROM incidents")
        get_list = (cursor_gt.fetchall())
        cursor_gt.close()
        con_gt.commit()
        con_gt.close()
        return get_list
