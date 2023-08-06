import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT, ISOLATION_LEVEL_DEFAULT
import json
from configparser import ConfigParser
import json
try:
    import importlib.resources as pkg_resources
    from . import static
    DIST_FLAG = 1
except:
    DIST_FLAG = 0

HOST = "localhost"

def config(file_name="database.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(file_name)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for i in params:
            db[i[0]] = i[1]
    return db

def config_create(file_name="database.ini", section="postgresql", host="localhost", database="geotag"):
    parser = ConfigParser()
    parser.read(file_name)
    parser.add_section(section)
    parser.set(section, "host", host)
    parser.set(section, "database", database)
    with open(file_name, "a") as inifile:
        parser.write(inifile)

def create_db(username="postgress", password=""):
    print("This script creates a database named geotag, It can not be used to update said database continue?:")
    x = input("y/n")
    if x == "y":
        connection = psycopg2.connect(host=HOST)
        try:
            connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = connection.cursor()
            cursor.execute("CREATE DATABASE geotag;")
            connection.close()
            config_create()
            db_parameters = config()
            connection = psycopg2.connect(**db_parameters)
            connection.set_isolation_level(ISOLATION_LEVEL_DEFAULT)
            cursor = connection.cursor()
            command = ("CREATE TABLE IF NOT EXISTS PictureReference(" +
            "id SERIAL PRIMARY KEY, original_name VARCHAR(200) NOT NULL, " +
            "temporary_name VARCHAR(200) NOT NULL, time_recieved " +
            "VARCHAR(100) NOT NULL);")
            cursor.execute(command)
            command = ("CREATE TABLE IF NOT EXISTS settings(" + 
            "id SERIAL PRIMARY KEY, key VARCHAR(100), value VARCHAR(100));")
            cursor.execute(command)
            command = ("INSERT INTO settings (key, value) VALUES(%s, %s)")
            cursor.execute(command, ("SCHEMA_VERSION", "0.0.0"))
            connection.commit()
        except:
            print("error in create_db TODO add more granular db handleing")
        finally:
            connection.close()
    else:
        exit()


def update_db():
    db_parameters = config()
    connection = psycopg2.connect(**db_parameters)
    try:
        cursor = connection.cursor()
        command = "SELECT value FROM settings WHERE key='SCHEMA_VERSION'"
        cursor.execute(command)
        version = cursor.fetchone()[0]
        if DIST_FLAG == 1:
            resource = json.loads(pkg_resources.read_text("static", "db_settings.txt"))
        else: 
            with open("/Users/alex/Documents/work/database_package/datclass/static/db_settings.txt") as static:
                resource = json.load(static)
        if version != resource["version"]:
            flag = False
            if version == "0.0.0":
                flag = True
            for i in resource["changelog"]:
                if i[0] == version:
                    flag = True
                if flag:
                    for key in i[1]:
                        print("hey!")
                        command = f"ALTER TABLE {key} {i[1][key]}"
                        cursor.execute(command)
                        command = f"UPDATE settings SET value='{resource['version']}' WHERE key='SCHEMA_VERSION'"
                        cursor.execute(command)
        connection.commit()
    except:
        print("error in db_update TODO add more granular error handling")
    finally:
        connection.close()


# TODO fix issue of using superuser to do things that superuser is not needed for,
# An issue has been caused where I can no longer drop db due to open connections
# Add Finally blocks to take care of this

def pip_test():
    print("successfully installed")
    return

