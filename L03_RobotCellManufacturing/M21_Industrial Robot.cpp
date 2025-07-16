#include <Servo.h>

// 서보모터 객체 생성
Servo servo_0;
Servo servo_1;
Servo servo_2;
Servo servo_3;
Servo servo_4;

int delayTime = 15;
int actionDelay = 1000;
int fmsDelay = 20000;

void setup() {
  Serial.begin(115200);  // 시리얼 통신 속도 설정

  // 서보모터 초기화
  servo_0.attach(3);
  servo_1.attach(5);
  servo_2.attach(6);
  servo_3.attach(9);  // ⚠ 서보모터 9번 핀 유지
  servo_4.attach(10);
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    input.trim();

    if (input == "시작") {
      runScenario();
    }
  }

  int motor_speed = analogRead(A0);  
  Serial.print("Motor Speed: ");
  Serial.println(motor_speed);
  delay(1000);  // 1초마다 측정
}

void runScenario() {
  // Base 단계
  moveServo(servo_1, 90);
  moveServo(servo_2, 90);
  moveServo(servo_3, 82);
  moveServo(servo_4, 90);
  moveServo(servo_0, 0);
  delay(actionDelay);

  // Home 단계
  moveServo(servo_4, 160);
  moveServo(servo_4, 150);
  moveServo(servo_1, 45);
  moveServo(servo_2, 85);
  delay(actionDelay);

  // 이동 단계
  moveServo(servo_1, 60);
  moveServo(servo_2, 100);
  moveServo(servo_1, 80);
  moveServo(servo_2, 120);
  moveServo(servo_4, 180);
  moveServo(servo_4, 167);
  delay(actionDelay);

  // FMS 1 단계
  moveServo(servo_0, 64);
  moveServo(servo_1, 60);
  delay(fmsDelay);

  // 이동 단계
  moveServo(servo_4, 180);
  moveServo(servo_4, 175);
  moveServo(servo_1, 85);
  moveServo(servo_2, 150);
  delay(actionDelay);

  // FMS 2 단계
  moveServo(servo_0, 120);
  moveServo(servo_2, 115);
  moveServo(servo_1, 60);
  moveServo(servo_4, 160);
  delay(fmsDelay);

  // 이동 단계
  moveServo(servo_4, 180);
  moveServo(servo_4, 175);
  moveServo(servo_1, 85);
  moveServo(servo_2, 150);
  delay(actionDelay);

  // FMS 3 단계
  moveServo(servo_0, 180);
  moveServo(servo_2, 115);
  moveServo(servo_1, 60);
  moveServo(servo_4, 160);
  delay(fmsDelay);

  // 이동 단계
  moveServo(servo_4, 180);
  moveServo(servo_4, 175);
  moveServo(servo_1, 85);
  moveServo(servo_2, 150);
  delay(actionDelay);

  // Return 단계
  moveServo(servo_0, 3);
  moveServo(servo_2, 120);
  moveServo(servo_1, 70);
  moveServo(servo_2, 100);
  moveServo(servo_1, 50);
  moveServo(servo_2, 80);
  moveServo(servo_1, 40);
  moveServo(servo_4, 150);
  delay(actionDelay);
  
  // Base 단계 (전자석 없이 종료)
  moveServo(servo_1, 90);
  moveServo(servo_2, 90);
  moveServo(servo_3, 82);
  moveServo(servo_4, 90);
  moveServo(servo_0, 0);
  delay(actionDelay);
}

// 서보모터 이동 함수
void moveServo(Servo &servo, int targetAngle) {
  int currentAngle = servo.read();
  if (currentAngle != targetAngle) {
    if (currentAngle < targetAngle) {
      for (int angle = currentAngle; angle <= targetAngle; angle++) {
        servo.write(angle);
        delay(delayTime);
      }
    } else {
      for (int angle = currentAngle; angle >= targetAngle; angle--) {
        servo.write(angle);
        delay(delayTime);
      }
    }
  }
}
