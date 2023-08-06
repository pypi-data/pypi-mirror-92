from dataclasses import dataclass
from datetime import datetime
import psycopg2
from datclass.db_func.config import config

@dataclass
class PictureReference:
    original_name: str
    temporary_name: str
    time_recieved: str

    def insert_reference(self):
        connection = None
        db_parameters = config()
        connection = psycopg2.connect(**db_parameters)
        cursor = connection.cursor()
        insert_command = ("INSERT INTO picturereference (original_name, temporary_name, time_recieved) VALUES(%s, %s, %s) RETURNING id;",
        (self.original_name, self.temporary_name, self.time_recieved, ))
        """ TODO add filesize(kb), and lat lng, filesize needs an update, change time to utc
            Look into exif data loss on upload change dropzone to go as soon as we get a drop"""
        cursor.execute(insert_command[0], insert_command[1])
        pic_id = cursor.fetchone()[0]
        connection.commit()
        if connection is not None:
            connection.close()
        return pic_id

    def create_table(self):
        pass

    def update_table(self):
        pass