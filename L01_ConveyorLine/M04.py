import RPi.GPIO as GPIO
import time
import logging
import MySQLdb

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

def insert_item_counts(good_count, bad_count):
    """아이템 카운트를 MariaDB에 삽입합니다."""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO color_counts (Accumulated_Red_Counts, Accumulated_Blue_Counts, Total)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (bad_count, good_count, good_count + bad_count))
        conn.commit()
        logging.info("아이템 카운트가 데이터베이스에 성공적으로 저장되었습니다.")
    except MySQLdb.Error as err:
        logging.error(f"데이터베이스 오류: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# 핀 설정
TRIG1 = 17  # GPIO 17 (핀 11)
ECHO1 = 27  # GPIO 27 (핀 13)
TRIG2 = 22  # GPIO 22 (핀 15)
ECHO2 = 23  # GPIO 23 (핀 16)

# 모터 드라이버 핀 설정
ENA = 0    # GPIO 0 (핀 27)
IN1 = 5    # GPIO 5 (핀 29)
IN2 = 6    # GPIO 6 (핀 31)

# GPIO 모드 설정
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# 핀 모드 설정
GPIO.setup(TRIG1, GPIO.OUT)
GPIO.setup(ECHO1, GPIO.IN)
GPIO.setup(TRIG2, GPIO.OUT)
GPIO.setup(ECHO2, GPIO.IN)

GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)

# PWM 설정
pwmA = GPIO.PWM(ENA, 100)  # 100Hz
pwmA.start(0)

# 모터를 앞으로 돌리기 위한 설정
GPIO.output(IN1, GPIO.LOW)
GPIO.output(IN2, GPIO.HIGH)
pwmA.ChangeDutyCycle(50)  # 모터 속도를 50%로 설정

def measure_distance(trigger, echo):
    GPIO.output(trigger, True)
    time.sleep(0.00001)
    GPIO.output(trigger, False)
    
    start_time = time.time()
    stop_time = time.time()
    
    while GPIO.input(echo) == 0:
        start_time = time.time()
    
    while GPIO.input(echo) == 1:
        stop_time = time.time()
    
    time_elapsed = stop_time - start_time
    distance = (time_elapsed * 34300) / 2
    return distance

def main():
    good_count = 0
    bad_count = 0

    # 초기 거리 측정
    initial_distance1 = measure_distance(TRIG1, ECHO1)
    initial_distance2 = measure_distance(TRIG2, ECHO2)

    logging.basicConfig(level=logging.INFO)
    logging.info("집계 시작")

    last_good_count = good_count
    last_bad_count = bad_count

    try:
        while True:
            distance1 = measure_distance(TRIG1, ECHO1)
            distance2 = measure_distance(TRIG2, ECHO2)
            
            if abs(distance1 - initial_distance1) > 1.2:  # 초기 거리와 다를 때
                good_count += 1
                print(f"Good: {good_count}, Bad: {bad_count}")
                initial_distance1 = distance1  # 초기 거리 업데이트
                time.sleep(2)  # 디바운싱을 위한 지연 시간
            
            if abs(distance2 - initial_distance2) > 1.2:  # 초기 거리와 다를 때
                bad_count += 1
                print(f"Good: {good_count}, Bad: {bad_count}")
                initial_distance2 = distance2  # 초기 거리 업데이트
                time.sleep(2)  # 디바운싱을 위한 지연 시간
            
            if good_count != last_good_count or bad_count != last_bad_count:
                insert_item_counts(good_count, bad_count)
                last_good_count = good_count
                last_bad_count = bad_count


            time.sleep(0.2)  # 100ms마다 거리 측정
    except KeyboardInterrupt:
        print("Program interrupted")
    finally:
        pwmA.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    main()
