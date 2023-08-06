from dataclasses import dataclass
from datetime import datetime
import psycopg2
import datetime
from dpl_geodb.geo_ops import config

@dataclass
class PictureReference:
    original_name: str
    temporary_name: str
    file_size: str
    time_recieved: str = datetime.datetime.now(datetime.timezone.utc)
    lat: str = ""
    lng: str = ""

    def insert_reference(self):
        connection = None
        db_parameters = config()
        connection = psycopg2.connect(**db_parameters)
        try:
            cursor = connection.cursor()
            insert_command = ("INSERT INTO picturereference (original_name, temporary_name, time_recieved) VALUES(%s, %s, %s) RETURNING id;",
            (self.original_name, self.temporary_name, self.time_recieved, ))
            cursor.execute(insert_command[0], insert_command[1])
            pic_id = cursor.fetchone()[0]
            connection.commit()
        except:
            return("Error")
        finally:
            if connection is not None:
                connection.close()
        return pic_id

