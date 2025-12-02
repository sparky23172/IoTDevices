"""
ESP32 CAPTURE AND CONVERT TO BINARY
MicroPython compatible - no step parameters
"""

from machine import Pin
import time

IR_RX_PIN = 14
sensor = Pin(IR_RX_PIN, Pin.IN)

def capture_signal():
    """Capture IR signal"""
    pulses = []
    
    print("Point remote and press button...")
    
    # Wait for signal
    timeout = time.ticks_add(time.ticks_ms(), 10000)
    while sensor.value() == 1:
        if time.ticks_diff(timeout, time.ticks_ms()) < 0:
            print("Timeout")
            return None
    
    print("Recording...")
    
    # Capture
    start = time.ticks_us()
    last_time = start
    last_state = sensor.value()
    
    while True:
        current = sensor.value()
        now = time.ticks_us()
        
        if current != last_state:
            duration = time.ticks_diff(now, last_time)
            if duration > 50:
                pulses.append(duration)
            last_time = now
            last_state = current
        
        if len(pulses) > 10:
            if time.ticks_diff(now, last_time) > 30000:
                break
        
        if time.ticks_diff(now, start) > 200000:
            break
    
    print("Captured {} pulses".format(len(pulses)))
    return pulses


def to_binary(signal):
    """Convert signal to binary - MicroPython compatible"""
    binary = ""
    i = 3
    
    while i < len(signal):
        if signal[i] > 1000:
            binary += '1'
        else:
            binary += '0'
        i = i + 2
    
    return binary


def decode_nec(binary):
    """Decode NEC protocol"""
    if len(binary) < 32:
        return None, None
    
    # Decode address (bits 0-7, LSB first)
    addr = 0
    for bit in range(8):
        if binary[bit] == '1':
            addr = addr + (1 << bit)
    
    # Decode command (bits 16-23, LSB first)
    cmd = 0
    for bit in range(8):
        if binary[16 + bit] == '1':
            cmd = cmd + (1 << bit)
    
    return addr, cmd


# Main loop
print("=" * 50)
print("IR CAPTURE TO BINARY - ESP32")
print("=" * 50)
print("")

while True:
    input("Press Enter to capture...")
    
    # Capture
    pulses = capture_signal()
    
    if not pulses or len(pulses) < 10:
        print("Signal too short")
        continue
    
    # Convert
    binary = to_binary(pulses)
    
    print("")
    print("Binary ({} bits):".format(len(binary)))
    print(binary[0:8])
    print(binary[8:16])
    print(binary[16:24])
    print(binary[24:32])
    print(binary)
    print("")
    
    # Decode
    addr, cmd = decode_nec(binary)
    
    if addr is not None:
        print("Address: 0x{:02X}".format(addr))
        print("Command: 0x{:02X}".format(cmd))
    
    print("")
    print("-" * 50)
    print("")
