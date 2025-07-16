import RPi.GPIO as GPIO
import time

# GPIO 핀 설정
IN1 = 17
IN2 = 18
ENA = 12

# GPIO 모드 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

# PWM 설정
pwm = GPIO.PWM(ENA, 1000)  # PWM 핀, 주파수 1kHz 설정
pwm.start(0)  # PWM 초기값 0%

# 모터 속도 설정 (0 ~ 100)
speed = 23

try:
    while True:
        # 모터 회전 설정
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        pwm.ChangeDutyCycle(speed)
        time.sleep(0.1)  # 잠시 대기

except KeyboardInterrupt:
    # 사용자가 Ctrl+C를 눌렀을 때 실행
    print("모터 중지")
    
finally:
    # 프로그램 종료 시 모터와 GPIO 설정 정리
    pwm.stop()
    GPIO.cleanup()