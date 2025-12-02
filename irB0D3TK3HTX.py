from machine import Pin, PWM
import time

IR_TX_PIN = 12

on =    '00000000111101111100000000111111'
off =   '00000000111101110100000010111111'
blue =  '00000000111101110101000010101111'
red =   '00000000111101110001000011101111'
white = '00000000111101110110000010011111'


def send_from_binary(bits, pin=12):
    """Reconstruct and send NEC signal from binary string"""
    pwm = PWM(Pin(pin))
    pwm.freq(38000)
    
    # Lead-in
    pwm.duty(512)
    time.sleep_us(9000)
    pwm.duty(0)
    time.sleep_us(4500)
    
    # Data bits
    print(bits)
    for bit in bits:
        pwm.duty(512)
        time.sleep_us(560)
        pwm.duty(0)
        
        if bit == '1':
            time.sleep_us(1690)
        else:
            time.sleep_us(560)
    
    # Final mark
    pwm.duty(512)
    time.sleep_us(560)
    pwm.duty(0)
    
def main():    
    send_from_binary(on, IR_TX_PIN)
    time.sleep(1)
    send_from_binary(blue, IR_TX_PIN)
    time.sleep(1)
    send_from_binary(white, IR_TX_PIN)
    time.sleep(1)
    send_from_binary(red, IR_TX_PIN)
    time.sleep(1)
    send_from_binary(off, IR_TX_PIN)

    print("Signals Sent!")

main()
