
import unittest
import datetime as dt
import random
import pandas as pd
import os
from pathlib import Path
from library.data_storage.stored_reading import StoredReadings
import sqlite3

class TestStoredReadings(unittest.TestCase):

    def setUp(self):
        pass

    # this also tests get number of readings
    def test_add_readings(self):
        print('Starting test add reading')
        aSR = StoredReadings()

        # Create data to send

        for i in range(0, 3, 1):
            x = random.randint(0, 359)
            y = random.randint(0, 359)
            z = random.randint(0, 359)

            aSR.add_readings("46406064", "faketime", x, y, z )

        n = aSR.get_number_of_readings()
        print('n = {}'.format(n))
        self.assertTrue(n == 2)

    def test_add_readings_to_db(self):
        print("Starting ADD readings to DB test")
        os.chdir('C:\\users\\shane\\documents\\code\\flask-pi-iot')
        print('This is the current working directory {}'.format(os.getcwd()))
        aSR = StoredReadings()
        initial_number = aSR.get_number_of_readings_from_db()
        print('Initial_number {}'.format(initial_number))
        for i in range(0, 3):
            x = random.randint(0, 358)
            y = random.randint(0, 358)
            z = random.randint(0, 358)
            d = dt.datetime.now()
            sn = "46406064"
            aSR.add_readings_to_db(sn, d, x, y, z)

        ending_number = aSR.get_number_of_readings_from_db()
        print('Ending_number {}'.format(ending_number))
        self.assertTrue(ending_number - initial_number == 3)

    def test_get_first_reading(self):
        print('Starting  getfirst reading test')
        aSR = StoredReadings()
        serialNumber = [100, 200, 300]

        for i in range(0, 3):
            x = random.randint(0, 359)
            y = random.randint(0, 359)
            z = random.randint(0, 359)

            aSR.add_readings(serialNumber[i], "faketime", x, y, z)

        fr = aSR.get_first_reading()

        self.assertTrue(type(fr) == dict)
        self.assertTrue(len(fr) == 6)
        self.assertTrue(fr['serial_no'] == 100)

    def test_get_next_reading(self):
        print('Strarting next reading test')
        aSR = StoredReadings()
        serialNumber = [100, 200, 300]

        for i in range(0, 3):
            x = random.randint(0, 359)
            y = random.randint(0, 359)
            z = random.randint(0, 359)

            aSR.add_readings(serialNumber[i], "faketime", x, y, z)

        fr = aSR.get_next_reading()

        self.assertTrue(type(fr) == dict)
        self.assertTrue(len(fr) == 6)
        self.assertTrue(fr['serial_no'] == 200)

    def test_get_previous_reading(self):
        print('Strarting previous reading test')
        aSR = StoredReadings()
        serialNumber = [100, 200, 300]

        for i in range(0, 3):
            x = random.randint(0, 359)
            y = random.randint(0, 359)
            z = random.randint(0, 359)

            aSR.add_readings(serialNumber[i], "faketime", x, y, z)

        first_reading = aSR.get_first_reading()
        get_next_reading = aSR.get_next_reading()
        fr = aSR.get_previous_reading()

        self.assertTrue(type(fr) == dict)
        self.assertTrue(len(fr) == 6)
        self.assertTrue(fr['serial_no'] == 100)
        self.assertTrue(fr == first_reading)

    # Pull a selection of entries between certian time periods
    def test_time_selection(self,):
        aSR = StoredReadings()
        serialNumber = [100, 200, 300, 400, 500]
        time = [1, 2, 3, 4, 5]

        for i in range(0, 3):
            x = random.randint(0, 359)
            y = random.randint(0, 359)
            z = random.randint(0, 359)

            aSR.add_readings(serialNumber[i], time[i], x, y, z)

        fr = aSR.time_selection(2, 4)

        self.assertTrue(len(fr) == 12)
        self.assertTrue()

    def test_push_to_s3(self,):
        # setup a dataframe
        column_title = ['people', 'places', 'numbers']
        data = [('david', 'italy', 4), ('megan', 'germany', 5), ('Katie', 'spain', 9), ('shane', 'norway', 3)]
        df = pd.DataFrame(data, columns=column_title)
        aSR = StoredReadings()

        aSR.push_to_s3(df)

    def test_get_df_from_db_by_serial_no(self):

        print("Starting get DF from DB test")
        os.chdir('C:\\users\\shane\\documents\\code\\flask-pi-iot')
        print('This is the current working directory {}'.format(os.getcwd()))
        aSR = StoredReadings()

        for i in range(0, 3):
            x = random.randint(0, 358)
            y = random.randint(0, 358)
            z = random.randint(0, 358)
            d = dt.datetime.now()
            sn = "DFTEST00"
            aSR.add_readings_to_db(sn, d, x, y, z)

        df = aSR.get_df_from_db_by_serial_no("DFTEST00")
        print('This is the Dataframe returned from the database {}'.format(df))

        conn = sqlite3.connect('data\\readings.db')
        cur = conn.cursor()
        sql_string = "DELETE FROM readings WHERE serial_no = 'DFTEST00'"
        cur.execute(sql_string)
        conn.commit()
        conn.close()

        self.assertTrue(df.shape[0] == 3)




if __name__ == '__main__':
    print('Starting the unittest')
    unittest.main()

