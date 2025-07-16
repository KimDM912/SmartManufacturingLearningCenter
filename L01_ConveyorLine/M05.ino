#include <Stepper.h>

// ✅ 28BYJ-48 스텝모터 설정 (ULN2003 사용)
#define MOTOR_PIN1 8
#define MOTOR_PIN2 9
#define MOTOR_PIN3 10
#define MOTOR_PIN4 11

Stepper myStepper(2048, MOTOR_PIN1, MOTOR_PIN2, MOTOR_PIN3, MOTOR_PIN4);

// ✅ DC 모터 (L298N 사용)
#define ENB 7    // DC 모터 속도 제어 (PWM)
#define IN3 5    // DC 모터 방향 제어 1
#define IN4 6    // DC 모터 방향 제어 2

// ✅ 72도 회전 스텝 순서 (직관적 설정)
const int stepValues[5] = {410, 409, 410, 409, 410};  
int rotationIndex = 0;  // 현재 몇 번째 회전인지 기록

void setup() {
    Serial.begin(115200);

    // ✅ DC 모터 핀 설정
    pinMode(ENB, OUTPUT);
    pinMode(IN3, OUTPUT);
    pinMode(IN4, OUTPUT);

    // ✅ 스텝모터 속도 설정 (속도를 5로 설정)
    myStepper.setSpeed(5);

    Serial.println("모터 동작 시작");

    // ✅ DC 모터 시작 (컨베이어 계속 동작)
    moveDCMotor(255);  // 속도 255 (최대 출력)
}

void loop() {
    Serial.print("스텝모터 72도 회전 시작 (");
    Serial.print(stepValues[rotationIndex]);
    Serial.println(" 스텝)");

    myStepper.step(stepValues[rotationIndex]);  // ✅ 현재 회전에서 정해진 스텝 수만큼 회전
    Serial.println("스텝모터 72도 회전 완료");

    // ✅ 다음 회전 값 선택 (5회 주기로 반복)
    rotationIndex++;
    if (rotationIndex >= 5) {
        rotationIndex = 0;  // 다시 처음부터 시작
    }

    delay(5000);  // 5초 대기 후 반복
}

// ✅ DC 모터 회전 함수 (L298N 사용)
void moveDCMotor(int speed) {
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
    analogWrite(ENB, speed); // 🔹 속도 조절 가능 (0~255)
}
