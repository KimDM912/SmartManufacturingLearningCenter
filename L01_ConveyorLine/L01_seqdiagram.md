```mermaid
sequenceDiagram
  participant M01 as M01 (Feeder)
  participant M02 as M02 (Conveyor)
  participant M03 as M03 (Classification)
  participant M04 as M04 (Counter)
  
  M01->>M01: Material Feeding
  M01->>M02: Material Output and Transfer
  M02->>M03: Material Movement
  M03->>M03: Stop Material with Servo Motor
  M03-->>M03: Detect Color with Camera
  M03-->>M03: Send Data
  M03->>M04: Operate Servo Motor for Sorting
  M04-->>M04: Counting
  M04->>M04: Material Sorting

  note right of M03: Color detection and data transmission
  note right of M04: Sorting and counting process
```

```mermaid
graph TD
    A[" "] -->|**Physical Movement**| B[" "]
    C[" "] -.->|**Information Transmission**| D[" "]

    %% 설명 박스 추가
    E["🔹 **Solid Line (→): Physical material movement**"]:::desc
    F["🔹 **Dashed Line (-.->): Information transmission**"]:::desc

    %% 박스를 스타일링 (노드로 보이지 않게)
    classDef desc fill:#fdf5a0,stroke:#000,stroke-width:1px,font-weight:bold
