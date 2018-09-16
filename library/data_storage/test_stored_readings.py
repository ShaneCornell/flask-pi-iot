
import unittest
import datetime
import random
from library.data_storage.stored_reading import StoredReadings

class TestStoredReadings(unittest.TestCase):

    def setUp(self):
        pass

    # this also tests get number of readings
    def test_add_readings(self):
        print('Starting test add reading')
        aSR = StoredReadings()

        # Create data to send

        for i in range(0, 3):
            x = random.randint(0, 359)
            y = random.randint(0, 359)
            z = random.randint(0, 359)

            aSR.add_readings("46406064", "faketime", x, y, z )

        n = aSR.get_number_of_readings()
        #print('n = {}'.format(n))
        self.assertTrue(n == 2)

    # def test_serial_no_data(self):
    #     print('Strarting serial number data test')
    #     aSR = StoredReadings()
    #     serialNumber = ['100', '200', '300']
    #
    #     for i in range(0, 3):
    #         x = random.randint(0, 359)
    #         y = random.randint(0, 359)
    #         z = random.randint(0, 359)
    #
    #         aSR.add_readings(serialNumber[i], "faketime", x, y, z)

    def test_get_first_reading(self):
        print('Strarting first reading test')
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

        fr = aSR.get_next_reading(0)

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

        fr = aSR.get_previous_reading(1)

        self.assertTrue(type(fr) == dict)
        self.assertTrue(len(fr) == 6)
        self.assertTrue(fr['serial_no'] == 100)

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


if __name__ == '__main__':
    print('Starting the unittest')
    unittest.main()

