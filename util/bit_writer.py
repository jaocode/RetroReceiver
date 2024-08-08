class BitWriter:
    def __init__(self, filename):
        self.filename = filename
        self.buffer = 0
        self.buffer_length = 0

    def write_bit(self, bit):
        if bit not in {0, 1}:
            raise ValueError("Bit must be 0 or 1")

        # Add bit to buffer
        self.buffer = (self.buffer << 1) | bit
        self.buffer_length += 1

        # If buffer contains a full byte, write to file
        if self.buffer_length == 8:
            self._flush_buffer()

    def _flush_buffer(self):
        with open(self.filename, 'ab') as f:
            f.write(bytes([self.buffer]))
        self.buffer = 0
        self.buffer_length = 0

    def close(self):
        # If there are remaining bits, pad with zeros and write
        if self.buffer_length > 0:
            self.buffer = self.buffer << (8 - self.buffer_length)
            self._flush_buffer()

# # Usage
# bit_writer = BitWriter('output.bin')

# # Simulate receiving bits
# bits = [1, 0, 1, 1, 0, 0, 1, 1,  # First byte (0b10110011)
#         0, 1, 0, 0, 1, 1, 1, 0,  # Second byte (0b01001110)
#         1, 0, 1, 1]              # Remaining bits (0b10110000, padded with 4 zeros)

# for bit in bits:
#     bit_writer.write_bit(bit)

# bit_writer.close()