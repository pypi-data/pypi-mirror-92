import adafruit_dht
from dbutils_phornee import homeTelemetryDB, DBOpenException
from baseutils_phornee import ManagedClass

class Sensors(ManagedClass):

    def __init__(self):
        super().__init__(execpath=__file__)
        self.homeDB = homeTelemetryDB()

    @classmethod
    def getClassName(cls):
        return "sensors"

    def sensorRead(self):
        """
        Read sensors information
        """
        try:
            conn = self.homeDB.openConn()
            cursor = conn.cursor()

            dhtSensor = adafruit_dht.DHT22(self.config['pin'])

            humidity = dhtSensor.humidity
            temp_c = dhtSensor.temperature

            if temp_c:
                # print(SENSOR_LOCATION_NAME + " Temperature(C) {}".format(temp_c))
                sql = "INSERT INTO hometelemetry.measurements VALUES (null, {}, UTC_TIMESTAMP(), {})".format(self.config['temp_id'], temp_c)
                cursor.execute(sql)

            if humidity:
                # print(SENSOR_LOCATION_NAME + " Humidity(%) {}".format(humidity,".2f"))
                sql = "INSERT INTO hometelemetry.measurements VALUES (null, {}, UTC_TIMESTAMP(), {})".format(self.config['humid_id'], humidity)
                cursor.execute(sql)

            conn.commit()

        except Exception as e:
            self.logger.error("RuntimeError: {}".format(e))


if __name__ == "__main__":
    sensors_instance = Sensors()
    sensors_instance.sensorRead()





