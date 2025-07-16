import cv2
import numpy as np
import RPi.GPIO as GPIO
import time
import threading
import logging
import MySQLdb
from picamera2 import Picamera2

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# MariaDB 연결 설정
db_config = {
    'user': 'AIIS',                # MariaDB 사용자 이름
    'passwd': 'AIISDBSERVER',      # MariaDB 비밀번호 (MySQLdb에서는 'passwd' 사용)
    'host': '192.168.0.2',         # MariaDB 서버 호스트
    'db': 'AIIS_DB',               # 데이터베이스 이름 (MySQLdb에서는 'db' 사용)
}

def get_db_connection():
    """MariaDB에 연결하고 연결 객체를 반환합니다."""
    return MySQLdb.connect(**db_config)

def insert_color_data(color_detected):
    """컬러 데이터를 MariaDB에 삽입합니다."""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO color_classification (detected_at, color_detected)
            VALUES (CURRENT_TIMESTAMP, %s)
        """
        cursor.execute(query, (color_detected,))
        conn.commit()
        logging.info("컬러 데이터가 데이터베이스에 성공적으로 저장되었습니다.")
    except MySQLdb.Error as err:
        logging.error(f"데이터베이스 오류: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# GPIO 설정
SERVO_PIN = 18  # 서보 모터 제어 핀
IN1 = 5
IN2 = 6
ENA = 0

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# 모터 드라이버 핀 설정
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
pwmA = GPIO.PWM(ENA, 100)  # 100Hz PWM
pwmA.start(0)

# 서보 모터 PWM 설정
GPIO.setup(SERVO_PIN, GPIO.OUT)
servo = GPIO.PWM(SERVO_PIN, 50)  # 50Hz PWM
servo.start(0)

def rotate_servo(angle):
    duty = angle / 18 + 2.5
    GPIO.output(SERVO_PIN, True)
    servo.ChangeDutyCycle(duty)
    time.sleep(0.5)
    GPIO.output(SERVO_PIN, False)
    servo.ChangeDutyCycle(0)

# 모터 구동 함수
def run_motor():
    try:
        logging.info("모터 동작 시작")
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        pwmA.ChangeDutyCycle(40)  # 모터 속도 설정
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.error("모터 동작 중 사용자에 의해 프로그램이 종료되었습니다.")
        sys.exit(1)
    finally:
        pwmA.stop()
        GPIO.cleanup()

# 색상 범위 설정 - track.py로 감지한 범위값 괄호 안에 넣어주면 됨
lower_red = np.array([108, 249, 233])
upper_red = np.array([179, 255, 255])
lower_blue = np.array([0, 197, 93])
upper_blue = np.array([89, 255, 225])

# 색상 감지 함수
def detect_color(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 빨간색 감지
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    _, mask1_red = cv2.threshold(mask_red, 254, 255, cv2.THRESH_BINARY)
    cnts_red, _ = cv2.findContours(mask1_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for c in cnts_red:
        if cv2.contourArea(c) > 600:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, "RED DETECTED", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            return 'Red'

    # 파란색 감지
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    _, mask1_blue = cv2.threshold(mask_blue, 254, 255, cv2.THRESH_BINARY)
    cnts_blue, _ = cv2.findContours(mask1_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for c in cnts_blue:
        if cv2.contourArea(c) > 600:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, "BLUE DETECTED", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            return 'Blue'

    return 'None'

def run_color_detection():
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
    picam2.start()

    try:
        logging.info("Color detection started")
        while True:
            frame = picam2.capture_array()
            frame = cv2.resize(frame, (640, 480))

            detected_color = detect_color(frame)

            if detected_color == 'Red':
                rotate_servo(145)
                time.sleep(0.5)
                rotate_servo(91)
                insert_color_data('Red')

            elif detected_color == 'Blue':
                rotate_servo(180)
                time.sleep(0.5)
                rotate_servo(91)
                insert_color_data('Blue')

            time.sleep(1)

    except KeyboardInterrupt:
        logging.info("Color detection interrupted by user.")
    finally:
        picam2.close()
        GPIO.cleanup()
        servo.stop()

if __name__ == "__main__":
    try:
        # 모터 및 색상 감지 스레드 실행
        motor_thread = threading.Thread(target=run_motor)
        motor_thread.daemon = True
        motor_thread.start()

        run_color_detection()
    except KeyboardInterrupt:
        logging.info("Program exited by user.")
        GPIO.cleanup()
        sys.exit(0)


