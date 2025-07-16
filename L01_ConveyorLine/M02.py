import RPi.GPIO as GPIO
import time
import threading

# 모터 드라이버 핀 설정
ENA = 0    # GPIO 0 (핀 27)
IN1 = 5    # GPIO 5 (핀 29)
IN2 = 6    # GPIO 6 (핀 31)

# GPIO 모드 설정
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.cleanup()

# 모터 핀 모드 설정
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)

# PWM 설정
pwmA = GPIO.PWM(ENA, 100)  # 100Hz

# 모터 제어 함수
def motor_control():
    pwmA.start(0)
    
    # 모터를 반대로 돌리기 위한 설정
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    pwmA.ChangeDutyCycle(37)  # 모터 속도를 60%로 설정

    try:
        while True:
            time.sleep(1)  # 모터가 계속 돌도록 무한 루프 유지
    except KeyboardInterrupt:
        print("Motor control interrupted")
    finally:
        pwmA.stop()
        GPIO.cleanup()

# 메인 함수
def main():
    try:
        motor_thread = threading.Thread(target=motor_control)
        motor_thread.start()
        motor_thread.join()
    except KeyboardInterrupt:
        print("Program interrupted")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()