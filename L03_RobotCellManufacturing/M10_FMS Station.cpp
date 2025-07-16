// 모터 A 핀 정의
const int ENA = 6;
const int IN1 = 7;
const int IN2 = 8;

// 초음파 센서 핀 정의
const int trigPinA = 2, echoPinA = 3;  // 모터 A 센서

// 거리 측정 변수
long durationA, distanceA;

// 모터 상태 변수
bool motorARunning = false, motorAReversing = true;  // 초기값: 후진부터 시작

unsigned long motorRunStartTimeA = 0;
const unsigned long motorRunDuration = 17000; // 17초 (전진/후진 각각)

void setup() {
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(trigPinA, OUTPUT);
  pinMode(echoPinA, INPUT);

  Serial.begin(115200);  // 통신 속도를 115200으로統一
}

void loop() {
  measureDistance(trigPinA, echoPinA, durationA, distanceA);

  Serial.print("A: ");
  Serial.println(distanceA); 

  unsigned long currentTime = millis();

  // 모터 A 제어 (후진 -> 전진)
  controlMotor(distanceA, motorARunning, motorAReversing, motorRunStartTimeA, ENA, IN1, IN2, currentTime);

  // 모터 속도 측정 예제 추가
  int motor_speed = analogRead(A0);
  Serial.print("Motor Speed: ");
  Serial.println(motor_speed);

  delay(100);
}

// 초음파 거리 측정 함수
void measureDistance(int trig, int echo, long &duration, long &distance) {
  digitalWrite(trig, LOW);
  delayMicroseconds(2);
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);
  duration = pulseIn(echo, HIGH);

  if (duration == 0) {
    distance = 999;  // 🛑 초음파 센서 오류 방지 (비정상 값 처리)
  } else {
    distance = (duration / 2) * 0.0344;
  }
}

// 모터 제어 함수 (후진 -> 전진 순서로 변경)
void controlMotor(long distance, bool &motorRunning, bool &motorReversing, unsigned long &motorRunStartTime, int EN, int IN1, int IN2, unsigned long currentTime) {
  if (motorRunning) {
    if (currentTime - motorRunStartTime > motorRunDuration) {
      if (motorReversing) {  // 후진 후 전진
        motorReversing = false;
        motorRunStartTime = currentTime;
        motorForward(EN, IN1, IN2, 255);  // 전진 (최대 속도)
      } else {  // 전진 후 정지
        motorRunning = false;
        motorReversing = true;  // 다음에 다시 후진부터 시작
        motorStop(EN, IN1, IN2);
        Serial.println("Motor stopped. Waiting for next trigger.");
        delay(500);
      }
    }
    return;
  }

  if (distance > 0 && distance < 7 && !motorRunning) {  // 7cm 이하 감지 시 동작
    Serial.println("Object detected! Motor starting...");
    motorRunning = true;
    motorReversing = true;  // 후진부터 시작
    motorRunStartTime = currentTime;
    motorReverse(EN, IN1, IN2, 255);  // 후진 (최대 속도)
  }
}

// 모터 제어 함수
void motorForward(int EN, int IN1, int IN2, int speed) { 
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  analogWrite(EN, speed);
  Serial.println("Motor moving forward.");
}

void motorReverse(int EN, int IN1, int IN2, int speed) { 
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  analogWrite(EN, speed);
  Serial.println("Motor moving backward.");
}

void motorStop(int EN, int IN1, int IN2) { 
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  analogWrite(EN, 0);
  Serial.println("Motor stopped.");
}
