# 화면 자동화 프로그램 개발 프롬프트 히스토리

## 사전단계: CHAT을 이용한 프로그램 설계
```
화면에서 이미지가 감지되면 클릭을 하도록 프로그램을 만들고 싶어. 

이미지 인식 -> 특정좌표클릭 ->잠시 멈추기 -> 특정좌표클릭

형태로 마우스를 제어할 수 있을까? 

좌표 클릭은 여러번할수도 있고 한번만 할수도 있어
```

### 라이브러리 설치: 
```
pip install pyautogui opencv-python pillow keyboard
```


## 1단계: 기본 이미지 감지 및 클릭
"화면의 특정 부분 이미지를 감지해야해"

## 2단계: 여러 클릭 위치 설정
"이제 클릭을 여러번 할 수 있게 추가해줘"

## 3단계: 트리거-액션 시스템
"좋아 이렇게 이미지를 찾아서 감지하고 클릭하는 과정을 트리거-액션 이라고 해볼께, 여러 이미지를 감지할 수 있도록 트리거-액션을 추가해줘"

## 4단계: 시나리오 관리 시스템
"이제 이렇게 설정한 트리거-액션 여러개를 '시나리오'라고 하고 저장해서 불러오면 좋겠어"

## 주요 기능 요구사항
1. 화면의 특정 영역을 감지하여 이미지로 저장
2. 여러 클릭 위치를 순서대로 저장하고 실행
3. 여러 트리거-액션을 하나의 시나리오로 관리
4. 시나리오 저장 및 로드 기능

## 사용자 인터랙션
- 오른쪽 마우스 버튼: 영역/위치 선택
- ESC 키: 선택 종료
- Ctrl+C: 실행 종료
