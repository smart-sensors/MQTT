def deserialize(bitstream):

    SENS_TYPE = 0
    DATA = 1
    NAME = 2

    bitstream = ''.join(bitstream)

    # split encoded message
    tokens = bitstream.split("_")
    sensor_type = tokens[SENS_TYPE]  # bytearray(tokens[SENS_TYPE]).decode()
    sensor_name = tokens[NAME]  # bytearray(tokens[NAME]).decode()
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


# TODO: Does this actually work? gattlib documentation doesn't specify return type of 'read'


if __name__ == "__main__":
    
    print(voltmeter2string(deserialize(['T', 'S', 'T', '_', '5', 'A', '_', 'T'])))
