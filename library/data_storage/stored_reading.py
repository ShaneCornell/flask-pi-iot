
import pandas as pd
import numpy as np

class StoredReadings():
    def __init__(self):
        self.df = []     # Create an empty dataframe
        self.df = pd.DataFrame(columns = ['serial_no', 'timestamp', 'x', 'y', 'z'])
        print(self.df)
        self.i = 0
        self.fileNumber = 0 #used for excel writer to increment filename

    # Method for adding a reading to the dataframe
    def add_readings(self, serial_no, ts, x, y, z):
        self.df = self.df.append({'serial_no': serial_no, 'timestamp': ts, 'x': x, 'y': y, 'z': z}, ignore_index=True)
        # To print each append data step, uncomment below
        # print(self.df)

    # Method for counting how many readings have been taken
    def get_number_of_readings(self):
        number_of_readings = self.df.index.max()
        return number_of_readings

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
        d = {'index': self.df.index[self.i], 'serial_no': self.df.serial_no[self.i], 'timestamp':self.df.timestamp[self.i], 'x': self.df.x[self.i], 'y': self.df.y[self.i],
             'z': self.df.z[self.i]}
        return d


    # Previous reading will return a dictionary with the previous reading
    def get_previous_reading(self):
        self.i = self.i - 1
        d = {'index': self.df.index[self.i], 'serial_no': self.df.serial_no[self.i], 'timestamp':self.df.timestamp[self.i], 'x': self.df.x[self.i], 'y': self.df.y[self.i],
             'z': self.df.z[self.i]}
        return d


    # Time selection will return a dictionary of readings and values between two different times.
    # Will it have to be a dictionary of dictionaries to handle multiple values?
    def time_selection(self, start_time, end_time):
        for row in self.df.iterrows():
            if df['timestamp'].between(start_time, end_time, inclusive = true) is True


    def readings_saver(self):
        n = self.get_number_of_readings()
        if n >= 1000:
            self.fileNumber = self.fileNumber + 1
            filename = 'Saved_Readings_' + str(self.fileNumber) + '.xlsx'
            print('Saving the last 1000 readings to {}'.format(filename))
            writer = pd.ExcelWriter(filename, engine='xlsxwriter')
            self.df.to_excel(writer, sheet_name='accelData')
            writer.save()
            self.df = []
            self.df = pd.DataFrame(columns=['serial_no', 'timestamp', 'x', 'y', 'z'])

    #when a specified number of readings are sent to server create csv and save in s3 bucket
    def push_to_s3(self, df):