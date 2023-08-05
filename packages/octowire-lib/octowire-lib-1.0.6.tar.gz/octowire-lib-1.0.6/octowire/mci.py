# -*- coding: utf-8 -*-

# Octowire Framework
# Copyright (c) ImmunIT - Jordan Ovrè / Paul Duncan
# License: Apache 2.0
# Paul Duncan / Eresse <pduncan@immunit.ch>
# Jordan Ovrè / Ghecko <jovre@immunit.ch>


import struct
from octowire.octowire import Octowire
from math import ceil


class MCI(Octowire):
    """
    MCI protocol class.
    The MCI protocol allows access to the Octowire's Memory Card interface.
    """
    OPCODE = b"\x0d"
    OPERATION_DETECT = b"\x01"
    OPERATION_TRANSMIT = b"\x02"
    OPERATION_RECEIVE = b"\x03"

    def __init__(self, serial_instance):
        """
        Init function.
        :param serial_instance: Octowire Serial instance.
        """
        self.serial_instance = serial_instance
        super().__init__(serial_instance=self.serial_instance)
        if not self.ensure_binary_mode():
            raise ValueError("Unable to enter binary mode.")

    def detect(self):
        """
        Detect MCI interface and return 4 Bytes containing Status, Type, Version and Capacity in KB information.
        return: Dictionary containing the status, type, version and capacity
        """
        valid_status = ["OK", "Initializing", "Error", "No media present"]
        valid_type = ["SD (Secure Digital)", "MMC (MultiMedia Card)", "SDHC (Secure Digital high Capacity)",
                      "MMCHC (MultiMedia Card High Capacity)", "SDIO (Secure Digital I/O)", "Combo (SD + SDIO)",
                      "Combo HC (SDHC + SDIO)", "Unknown"]
        args_size = struct.pack("<H", 1)
        self.serial_instance.write(args_size + self.OPCODE + self.OPERATION_DETECT)
        self._read_response_code(operation_name="MCI Detect response code")
        # Read values
        status = struct.unpack("<B", self.serial_instance.read(1))
        mem_type = struct.unpack("<B", self.serial_instance.read(1))
        version = struct.unpack("<B", self.serial_instance.read(1))
        capacity = struct.unpack("<L", self.serial_instance.read(4))
        # Data interpretation
        try:
            status_str = valid_status[status[0]]
        except KeyError:
            status_str = "Invalid status"
        try:
            type_str = valid_type[mem_type[0]]
        except KeyError:
            type_str = "Invalid type"
        return {
            "status": status[0],
            "status_str": status_str,
            "type": mem_type[0],
            "type_str": type_str,
            "minor_version": version[0] >> 0 & 0b1111,
            "major_version": version[0] >> 4 & 0b1111,
            "version_str": "{}.{}".format(version[0] >> 4 & 0b1111, version[0] >> 0 & 0b1111),
            "capacity": capacity[0],
        }

    def _transmit_op(self, data, block_nb):
        """
        Craft the structure and send it to the Octowire hardware to write into the Memory Card.
        :param data: the data (bytes) to send through the MCI interface.
        :param block_nb: The index of the block to write.
        """
        args_size = struct.pack("<H", 5 + len(data))
        self.serial_instance.write(args_size + self.OPCODE + self.OPERATION_TRANSMIT +
                                   struct.pack("<L", block_nb) + data)
        self._read_response_code(operation_name="MCI transmit response code")

    def transmit(self, data, start_addr, keep_existing=True):
        """
        Transmit data through the MCI interface.
        :param data: the data (bytes) to send through the MCI interface.
        :param start_addr: The address at which to start writing.
        :param keep_existing: If true, keep any pre-existing when writing incomplete blocks.
        :return: Nothing
        """
        if not isinstance(data, bytes):
            raise ValueError("'data' parameter is not a bytes instance.")

        # Calculate the first block index and the offset
        # 1 block = 512 Bytes
        start_block = start_addr // 512
        offset = start_addr % 512

        # Calculate the number of blocks to write
        block_count = ceil(len(data) / 512)
        if offset > 0 and len(data) > (512 - offset):
            block_count += 1

        current_block = start_block
        chunk_index = 0
        while block_count > 0:
            # If there is an offset, start processing the first block.
            if offset:
                data_chunk = data[:512 - offset]
                data = data[512 - offset:]
                # Keep not overwritten block's data
                if keep_existing:
                    first_block = self.receive(512, current_block)
                    # Keep the end of the block (if there is not enough data)
                    if offset + len(data_chunk) < 512:
                        data_chunk = data_chunk + first_block[offset+len(data_chunk):]
                    # Keep the start of the block
                    data_chunk = first_block[:offset] + data_chunk
                else:
                    data_chunk = b"\x00" * offset + data_chunk
                # Writing the first block to the Memory Card
                self._transmit_op(data_chunk, current_block)
                offset = None
                # Update current block
                current_block = current_block + 1
                # Decrement number of block
                block_count = block_count - 1
            else:
                # Write 8 blocks maximum per transmission
                blocks = 8 if block_count > 8 else block_count
                data_chunk = data[chunk_index * 512:(chunk_index + blocks) * 512]
                # If there is not enough data to fill the block entirely and keep_data parameter is True
                if keep_existing and len(data_chunk) < (blocks * 512):
                    # Read the last block (for completion)
                    last_block = self.receive(512, current_block + (blocks - 1))
                    if blocks > 1:
                        # Write all the blocks except the latest which needs to be merge to existing data.
                        self._transmit_op(data_chunk[:(blocks - 1) * 512], current_block)
                        last_chunk_len = len(data_chunk[(blocks - 1) * 512:])
                        # Completing the last block to write with existing data
                        data_chunk = data_chunk[(blocks - 1) * 512:] + last_block[last_chunk_len:]
                    else:
                        last_chunk_len = len(data_chunk)
                        # Completing the last block to write with existing data
                        data_chunk = data_chunk + last_block[last_chunk_len:]
                    # Writing the last completed block to the Memory Card
                    self._transmit_op(data_chunk, current_block + (blocks - 1))
                else:
                    self._transmit_op(data_chunk, current_block)
                # Update current_block and chunk_index
                current_block = current_block + blocks
                chunk_index = chunk_index + blocks
                # Decrement number of block
                block_count = block_count - blocks

    def receive(self, size, start_addr):
        """
        This function receives the number of bytes from the MCI interface (starting at the defined address).
        :param size: the number of bytes to receive.
        :param start_addr: The address at which to start reading.
        :return: the read bytes.
        :rtype: bytes
        """
        data = bytearray()
        if not isinstance(size, int):
            raise ValueError("'size' parameter is not an integer.")
        args_size = struct.pack("<H", 6)

        # Calculate the first block index and the offset
        # 1 block = 512 Bytes
        start_block = start_addr // 512
        offset = start_addr % 512

        # Calculate the number of blocks to read
        block_count = ceil(size / 512)
        if offset > 0 and size > (512 - offset):
            block_count += 1

        current_block = start_block
        while block_count > 0:
            # Read by block of 8 maximum
            blocks = block_count if block_count < 8 else 8
            self.serial_instance.write(args_size + self.OPCODE + self.OPERATION_RECEIVE +
                                       struct.pack("<L", current_block) + struct.pack("<B", blocks))
            self._read_response_code(operation_name="MCI receive response code")
            if offset:
                data.extend(self._read_data(operation_name="MCI receive data")[offset:])
                offset = None
            else:
                data.extend(self._read_data(operation_name="MCI receive data"))
            # Update the index of the current block
            current_block = current_block + blocks
            # Decrement the size
            block_count = block_count - blocks
        return data[:size]
