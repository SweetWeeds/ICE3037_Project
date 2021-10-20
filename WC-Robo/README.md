# WC-Robo
## 개요
자율주행 무선충전 로봇의 제어를 위한 프로젝트이다.<br>
이를 위해 다음과 같은 파트로 기능이 나누어진다.
1. Drive: 자율주행 코드
2. Request: Core Server에서의 요청 수신 및 처리
3. Charge: 충전부 제어 코드

위 기능들은 모두 개별적으로 동시에 동작해야하므로 threading 혹은 asyncio 모듈을 사용하도록 한다.

## 요구사항
Python 3.8 이상