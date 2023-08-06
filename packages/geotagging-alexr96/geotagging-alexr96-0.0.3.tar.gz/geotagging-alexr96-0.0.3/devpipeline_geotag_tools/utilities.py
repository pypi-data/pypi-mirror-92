from configparser import ConfigParser
import json

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