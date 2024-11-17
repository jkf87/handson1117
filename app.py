import pyautogui
import cv2
import numpy as np
import time
from PIL import ImageGrab
import win32api
import win32con
import json
import os

class TriggerAction:
    def __init__(self, trigger_image, click_positions):
        self.trigger_image = trigger_image
        self.click_positions = click_positions

class Scenario:
    def __init__(self, name, trigger_actions=None):
        self.name = name
        self.trigger_actions = trigger_actions or []
    
    def save(self):
        scenario_data = {
            'name': self.name,
            'trigger_actions': [
                {
                    'trigger_image': action.trigger_image,
                    'click_positions': action.click_positions
                }
                for action in self.trigger_actions
            ]
        }
        
        filename = f'scenario_{self.name}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(scenario_data, f, ensure_ascii=False, indent=2)
        print(f"\n시나리오가 {filename}로 저장되었습니다.")
    
    @classmethod
    def load(cls, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            scenario = cls(data['name'])
            for action_data in data['trigger_actions']:
                # 이미지 파일 존재 확인
                if not os.path.exists(action_data['trigger_image']):
                    print(f"오류: {action_data['trigger_image']} 파일을 찾을 수 없습니다.")
                    return None
                
                trigger_action = TriggerAction(
                    action_data['trigger_image'],
                    action_data['click_positions']
                )
                scenario.trigger_actions.append(trigger_action)
            
            return scenario
        except Exception as e:
            print(f"시나리오 로드 중 오류 발생: {e}")
            return None

def wait_for_right_click():
    """오른쪽 마우스 클릭을 기다리고 클릭 위치를 반환"""
    while True:
        if win32api.GetAsyncKeyState(win32con.VK_RBUTTON) < 0:  # 오른쪽 마우스 버튼
            x, y = pyautogui.position()
            time.sleep(0.1)  # 클릭 중복 방지
            return (x, y)
        if win32api.GetAsyncKeyState(win32con.VK_ESCAPE) < 0:  # ESC 키
            return None
        time.sleep(0.1)

def get_search_area():
    print("1. 오른쪽 마우스 버튼으로 검색할 영역의 왼쪽 상단을 클릭하세요.")
    start_pos = wait_for_right_click()
    if not start_pos:
        return None, None
    
    print("2. 오른쪽 마우스 버튼으로 검색할 영역의 오른쪽 하단을 클릭하세요.")
    end_pos = wait_for_right_click()
    if not end_pos:
        return None, None
    
    # 화면 크기 가져오기
    screen_width, screen_height = pyautogui.size()
    
    # 좌표 보정
    x1 = max(0, min(start_pos[0], end_pos[0]))
    y1 = max(0, min(start_pos[1], end_pos[1]))
    x2 = min(screen_width, max(start_pos[0], end_pos[0]))
    y2 = min(screen_height, max(start_pos[1], end_pos[1]))
    
    # 최소 크기 확인
    if x2 - x1 < 1 or y2 - y1 < 1:
        print("오류: 선택한 영역이 너무 작습니다.")
        return None, None
    
    return (x1, y1), (x2, y2)

def capture_click_positions():
    click_positions = []
    print("4. 클릭할 위치들을 순서대로 오른쪽 마우스 버튼으로 선택하세요. (ESC 키를 누르면 선택 종료)")
    
    while True:
        click_pos = wait_for_right_click()
        if click_pos is None:  # ESC 키를 누른 경우
            break
        click_positions.append(click_pos)
        print(f"클릭 위치 {len(click_positions)} 저장됨: {click_pos}")
    
    if not click_positions:
        print("클릭 위치가 선택되지 않았습니다.")
        return None
    
    print(f"총 {len(click_positions)}개의 클릭 위치가 저장되었습니다.")
    return click_positions

def capture_trigger_actions():
    trigger_actions = []
    first_time = True
    
    while True:
        if not first_time:
            print("\n다른 트리거-액션을 추가하시겠습니까?")
            print("1: 추가")
            print("2: 종료")
            
            try:
                choice = input("선택: ").strip()
                if choice == '2':
                    break
                elif choice != '1':
                    print("잘못된 입력입니다. 1 또는 2를 입력하세요.")
                    continue
            except:
                print("잘못된 입력입니다. 1 또는 2를 입력하세요.")
                continue
        
        first_time = False
        print("\n새로운 트리거-액션 설정을 시작합니다...")
        
        # 1-2. 검색 영역 설정
        while True:
            start_pos, end_pos = get_search_area()
            if start_pos is not None and end_pos is not None:
                break
            print("영역 선택을 다시 시도합니다...")
        
        # 이미지 파일명 생성
        trigger_image = f'trigger_image_{len(trigger_actions)}.png'
        print(f"3. 선택한 영역을 {trigger_image}로 저장합니다...")
        
        try:
            x1, y1 = start_pos
            x2, y2 = end_pos
            screenshot = pyautogui.screenshot(region=(x1, y1, x2-x1, y2-y1))
            screenshot.save(trigger_image)
            print("이미지가 저장되었습니다.")
        except Exception as e:
            print(f"이미지 저장 중 오류 발생: {e}")
            continue
        
        # 4. 클릭 위치들 설정
        while True:
            click_positions = capture_click_positions()
            if click_positions is not None:
                break
            print("클릭 위치 선택을 다시 시도합니다...")
            
        # 트리거-액션 저장
        trigger_action = TriggerAction(
            trigger_image=trigger_image,
            click_positions=click_positions
        )
        trigger_actions.append(trigger_action)
        print(f"\n트리거-액션 {len(trigger_actions)}이(가) 저장되었습니다.")
    
    return trigger_actions

def main():
    pyautogui.FAILSAFE = True
    
    while True:
        print("\n=== 자동화 시나리오 관리 ===")
        print("1: 새 시나리오 만들기")
        print("2: 기존 시나리오 실행")
        print("3: 종료")
        
        try:
            choice = input("선택: ").strip()
            
            if choice == '1':
                # 새 시나리오 생성
                name = input("\n시나리오 이름을 입력하세요: ").strip()
                if not name:
                    print("올바른 이름을 입력하세요.")
                    continue
                
                print("\n트리거-액션 설정을 시작합니다...")
                trigger_actions = capture_trigger_actions()
                
                if not trigger_actions:
                    print("설정된 트리거-액션이 없습니다.")
                    continue
                
                scenario = Scenario(name, trigger_actions)
                scenario.save()
                
            elif choice == '2':
                # 기존 시나리오 목록 표시
                scenario_files = [f for f in os.listdir() if f.startswith('scenario_') and f.endswith('.json')]
                if not scenario_files:
                    print("\n저장된 시나리오가 없습니다.")
                    continue
                
                print("\n=== 저장된 시나리오 ===")
                for i, filename in enumerate(scenario_files, 1):
                    print(f"{i}: {filename}")
                
                try:
                    idx = int(input("\n실행할 시나리오 번호를 선택하세요: ")) - 1
                    if not (0 <= idx < len(scenario_files)):
                        print("올바른 번호를 입력하세요.")
                        continue
                    
                    scenario = Scenario.load(scenario_files[idx])
                    if scenario:
                        print(f"\n'{scenario.name}' 시나리오를 실행합니다...")
                        print("모니터링을 시작합니다... (종료하려면 Ctrl+C)")
                        
                        while True:
                            try:
                                for idx, trigger_action in enumerate(scenario.trigger_actions):
                                    if find_and_click_image(
                                        trigger_action.trigger_image,
                                        search_area=None,
                                        click_positions=trigger_action.click_positions,
                                        clicks=1,
                                        delay_between_clicks=1
                                    ):
                                        print(f"트리거-액션 {idx+1}이(가) 실행되었습니다!")
                                        time.sleep(3)
                                time.sleep(1)
                            except KeyboardInterrupt:
                                print("\n시나리오 실행을 종료합니다.")
                                break
                except ValueError:
                    print("올바른 번호를 입력하세요.")
                    
            elif choice == '3':
                print("\n프로그램을 종료합니다.")
                break
                
            else:
                print("올바른 메뉴를 선택하세요.")
                
        except Exception as e:
            print(f"오류 발생: {e}")

def find_and_click_image(image_path, search_area=None, click_positions=None, clicks=1, delay_between_clicks=1):
    template = cv2.imread(image_path)
    if template is None:
        print(f"오류: {image_path} 파일을 찾을 수 없습니다.")
        return False
    
    try:
        if search_area is None:
            # 전체 화면 캡처
            screenshot = pyautogui.screenshot()
            screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        else:
            x1, y1 = search_area[0]
            x2, y2 = search_area[1]
            screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
            screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        threshold = 0.8
        if max_val >= threshold:
            for click_pos in click_positions:
                for _ in range(clicks):
                    pyautogui.click(click_pos)
                    time.sleep(delay_between_clicks)
            return True
        return False
    except cv2.error as e:
        print(f"OpenCV 오류: {e}")
        return False

if __name__ == "__main__":
    main()
