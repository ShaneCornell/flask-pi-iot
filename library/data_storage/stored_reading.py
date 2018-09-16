
import pandas as pd
import numpy as np

class StoredReadings():
    def __init__(self):
        self.df = []     # Create an empty dataframe
        self.df = pd.DataFrame(columns = ['serial_no', 'timestamp', 'x', 'y', 'z'])
        print(self.df)

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
        d = {'index':self.df.index[i], 'serial_no': self.df.serial_no[i], 'timestamp': self.df.timestamp[i], 'x': self.df.x[i], 'y': self.df.y[i],
             'z': self.df.z[i]}
        return d


    # Next reading will return a dictionary with the next reading
    def get_next_reading(self, index_no): # Incoming index_no must be an integer
        index_no = index_no + 1
        d = {'index': self.df.index[index_no], 'serial_no': self.df.serial_no[index_no], 'timestamp':self.df.timestamp[index_no], 'x': self.df.x[index_no], 'y': self.df.y[index_no],
             'z': self.df.z[index_no]}
        return d


    # Previous reading will return a dictionary with the previous reading
    def get_previous_reading(self, index_no):
        index_no = index_no - 1
        d = {'index': self.df.index[index_no], 'serial_no': self.df.serial_no[index_no], 'timestamp':self.df.timestamp[index_no], 'x': self.df.x[index_no], 'y': self.df.y[index_no],
             'z': self.df.z[index_no]}
        return d


    # Time selection will return a dictionary of readings and values between two different times.
    # Will it have to be a dictionary of dictionaries to handle multiple values?
    def time_selection(self, start_time, end_time):
        for row in self.df.iterrows():
            if df['timestamp'].between(start_time, end_time, inclusive = true) is True
