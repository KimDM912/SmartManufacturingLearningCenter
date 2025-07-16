# MiniFactory


## L03: Robot Cell Manufacturing

```mermaid
sequenceDiagram
    participant IN/OUT
    participant Robot_Arm
    participant Station_1
    participant Station_2
    participant Station_3

    Robot_Arm->>Station_1: Tranfer
    Station_1->>Station_1: Process 1 (15s)
    Station_1->>Robot_Arm: Transfer

    Robot_Arm->>Station_2: Tranfer
    Station_2->>Station_2: Process 2 (15s)
    Station_2->>Robot_Arm: Tranfer

    Robot_Arm->>Station_3: Tranfer
    Station_3->>Station_3: Process 3 (17s)
    Station_3->>Robot_Arm: Tranfer

    Robot_Arm->>IN/OUT: Tranfer & Discharge