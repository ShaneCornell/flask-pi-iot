
import pandas as pd
import numpy as np
import boto3
import sqlite3

class StoredReadings():
    def __init__(self):
        self.df = []     # Create an empty dataframe
        self.df = pd.DataFrame(columns = ['serial_no', 'timestamp', 'x', 'y', 'z'])
        #print(self.df)
        self.i = 0
        self.fileNumber = 0 #used for excel writer to increment filename

    # Method for adding a reading to the dataframe
    def add_readings(self, serial_no, ts, x, y, z):
        self.df = self.df.append({'serial_no': serial_no, 'timestamp': ts, 'x': x, 'y': y, 'z': z}, ignore_index=True)
        # To print each append data step, uncomment below
        print(self.df)
        self.aws_readings_saver()

    def add_readings_to_db(self, serial_no, ts, x, y, z):
        conn = sqlite3.connect('data\\readings.db')
        cur = conn.cursor()
        sql_string = "insert into readings (serial_no, timestamp, x, y, z) values ('{0}','{1}','{2}','{3}','{4}');".format(serial_no, ts, x, y, z)
        cur.execute(sql_string)
        conn.commit()
        conn.close()

    def get_all_data_as_list(self):
        dataList = []
        one = self.get_first_reading()
        dataList.append(one)
        while True:
            try:
                nextReading = self.get_next_reading()
                dataList.append(nextReading)
            except Exception as ex:
                # print("We got an unexpected error {}.".format(ex))
                return dataList

    # Method for counting how many readings have been taken
    def get_number_of_readings(self):
        number_of_readings = self.df.index.max()
        return number_of_readings

    def get_number_of_readings_from_db(self):
        conn = sqlite3.connect('data\\readings.db')
        cur = conn.cursor()
        cur.execute('select count(*) from readings;')
        result = cur.fetchall()
        count = result[0][0]
        conn.commit()
        conn.close()
        return count

    # Added index to "get first reading" so once next and, previous reading are usable it gives a easy way to find a row
    # Would it be better to keep track of which row is displayed on the back end or when next and previous are used
    # have the front end send back the index value out of the original returned dictionary?
    def get_first_reading(self):
        i = 0
        sizeOfDataFrame = self.df.shape[0]
        if sizeOfDataFrame > 0:
            d = {'index':self.df.index[self.i], 'serial_no': self.df.serial_no[self.i], 'timestamp': self.df.timestamp[self.i], 'x': self.df.x[self.i], 'y': self.df.y[self.i],
                 'z': self.df.z[self.i]}
        else:
            d = {'serial_no': "None", 'timestamp': "None", 'x': 0, 'y': 0, 'z': 0}
        return d


    # Next reading will return a dictionary with the next reading
    def get_next_reading(self): # Incoming index_no must be an integer
        self.i = self.i + 1
        d = {'index': self.df.index[self.i],
             'serial_no': self.df.serial_no[self.i],
             'timestamp':self.df.timestamp[self.i],
             'x': self.df.x[self.i],
             'y': self.df.y[self.i],
             'z': self.df.z[self.i]}
        return d


    # Previous reading will return a dictionary with the previous reading
    def get_previous_reading(self):
        self.i = self.i - 1
        d = {'index': self.df.index[self.i],
             'serial_no': self.df.serial_no[self.i],
             'timestamp': self.df.timestamp[self.i],
             'x': self.df.x[self.i],
             'y': self.df.y[self.i],
             'z': self.df.z[self.i]}
        return d

    def get_all_data_as_list(self):
        datalist = []
        first = self.get_first_reading()
        datalist.append(first)

        while True:
            try:
                somethingelse = self.get_next_reading()
                datalist.append(somethingelse)
            except Exception as ex:
                return datalist

    # def readings_saver(self):
    #     n = self.get_number_of_readings()
    #     if n >= 1000:
    #         self.fileNumber = self.fileNumber + 1
    #         filename = 'Saved_Readings_' + str(self.fileNumber) + '.xlsx'
    #         print('Saving the last 1000 readings to {}'.format(filename))
    #         writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    #         self.df.to_excel(writer, sheet_name='accelData')
    #         writer.save()
    #         self.df = []
    #         self.df = pd.DataFrame(columns=['serial_no', 'timestamp', 'x', 'y', 'z'])
    #         s3 = boto3.resource('s3')
    #         s3.meta.client.upload_file(filename, 'shanefirstbucket', filename)
    #
    # #when a specified number of readings are sent to server create csv and save in s3 bucket

    def aws_readings_saver(self):
        bucket = "shanefirstbucket"
        n = self.get_number_of_readings()
        if n >= 1000:
            self.fileNumber = self.fileNumber + 1
            filename = 'Saved_Readings_' + str(self.fileNumber) + '.csv'
            data_string = self.df.to_csv()
            s3 = boto3.resource('s3')
            s3.Bucket(bucket).put_object(Key = filename, Body = data_string)
            self.df = []
            self.df = pd.DataFrame(columns = ['serial_no', 'timestamp', 'x', 'y', 'z'])

    def get_df_from_db_by_serial_no(self, serial_no):
        conn = sqlite3.connect('data\\readings.db')
        sql_string = "SELECT * FROM readings WHERE serial_no = '{}'".format(serial_no)
        df = pd.read_sql_query(sql_string, conn)
        conn.close()

        return df


if __name__ == '__main__':
    aSR = StoredReadings()