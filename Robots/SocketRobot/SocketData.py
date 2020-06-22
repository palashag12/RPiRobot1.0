class SocketSpeedData(object):
    """speed data that is sent over sockets from client to pi"""

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def toBytes(self):
        leftByte = int(round(self.left * 127)).to_bytes(1, 'big', signed = True)
        rightByte = int(round(self.right * 127)).to_bytes(1, 'big', signed = True)
        return (leftByte + rightByte)

    def fromBytes(bytes):
        leftByte = bytes[0]
        rightByte = bytes[1]
        if leftByte > 127:
           left = (256-leftByte) * (-1)
        else:
           left = leftByte
        if rightByte > 127:
           right = (256-rightByte) * (-1) 
        else:
           right = rightByte 
        return SocketSpeedData(left / 127, right / 127)




