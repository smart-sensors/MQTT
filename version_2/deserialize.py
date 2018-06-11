def deserialize(bitstream):

    SENS_TYPE = 0
    DATA = 1
    NAME = 2

    # split encoded message
    tokens = bitstream.split("5F")
    sensor_type = bytearray.fromhex(tokens[SENS_TYPE]).decode()
    sensor_name = bytearray.fromhex(tokens[NAME]).decode()
    data_bytes = bytearray.fromhex(tokens[DATA])

    # rebuild data by reversing 'endianness'
    val = 0
    cnt = 0
    
    for x in data_bytes:
        val |= x << (cnt * 8)
        cnt += 1

    # convert to tuple
    return (sensor_type, val, sensor_name)

def voltmeter2string(sensor_tuple):
    return "Voltmeter {}: {} Volts".format(sensor_tuple[2], sensor_tuple[1] / 1000)


# TODO: What if data's value is 5F?



if __name__ == "__main__":
    
    print(voltmeter2string(deserialize("505F00FF5F51")))
