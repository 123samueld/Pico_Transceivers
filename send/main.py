from machine import Pin, SPI
import struct
from time import sleep

from nrf24l01 import NRF24L01

se = Pin(0, mode=Pin.OUT, value=0)   # Slave Enable (SE) Physical 1
ss = Pin(1, mode=Pin.OUT, value=1)   # Slave Select (SS) Physical 2
sck = Pin(2)                       # Serial Clock (SCK) Physical 4
mosi = Pin(3)                     # Master Out Slave In (MOSI) Physical 5
miso = Pin(4)                     # Master In Slave Out (MISO) Physical 6
led = Pin(25, Pin.OUT)
led.value(1)

# Addresses are in little-endian format. They correspond to big-endian
# 0xf0f0f0f0e1, 0xf0f0f0f0d2 - swap these on the other Pico!
# Com 7
pipes = (b"\xe1\xf0\xf0\xf0\xf0", b"\xd2\xf0\xf0\xf0\xf0")

def setup():
    nrf = NRF24L01(SPI(0, baudrate=4000000, sck=sck, mosi=mosi, miso=miso), ss, se, payload_size=4)
    
    nrf.open_tx_pipe(pipes[0])
    nrf.open_rx_pipe(1, pipes[1])
    nrf.start_listening()

    led.toggle()
    sleep(0.3)
    print("Setup completed")
    return nrf

def demo(nrf):
    print("Sending initial message")
    result = None
    try:
        result = nrf.send(struct.pack("i", 1))
    except OSError:
        print('Message lost')

    if result is None:
        print("Send operation in progress")
    elif result == 1:
        print("Message sent successfully")
    elif result == 2:
        print("Send failed: Maximum retries reached")


def auto_ack(nrf):
    nrf.reg_write(0x01, 0b11111000)  # enable auto-ack on all pipes

nrf = setup()
auto_ack(nrf)
demo(nrf)

