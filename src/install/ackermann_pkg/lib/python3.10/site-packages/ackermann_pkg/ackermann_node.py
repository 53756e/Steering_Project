import math
# =====================================================================
# [ROS 2 추가분 1] ROS 2 시스템을 파이썬으로 다루기 위한 핵심 라이브러리들입니다.
# =====================================================================
import rclpy
from rclpy.node import Node

# 아커만 기하학 계산 수식 (기존 코드와 완벽히 똑같습니다!)
def calculate_ackermann(steering_angle_deg, wheelbase=1.4, tread=0.42):
    alpha = math.radians(steering_angle_deg)
    if steering_angle_deg == 0:
        return 0.0, 0.0
    R = wheelbase / math.tan(alpha)
    delta_inside_rad = math.atan(wheelbase / (R - (tread / 2)))
    delta_outside_rad = math.atan(wheelbase / (R + (tread / 2)))
    return math.degrees(delta_inside_rad), math.degrees(delta_outside_rad)


# =====================================================================
# [ROS 2 추가분 2] ROS 2는 모든 프로그램을 '클래스(Class)'와 '노드(Node)' 형태로 만듭니다.
# =====================================================================
class AckermannSimulatorNode(Node):
    def __init__(self):
        # 'ackermann_node'라는 이름으로 ROS 2 시스템에 등록합니다.
        super().__init__('ackermann_node')
        
        # 터미널 창에 프로그램이 잘 켜졌다고 알리는 안내 문구(로그)를 출력합니다.
        self.get_logger().info('=========================================')
        self.get_logger().info('  ROS 2 아커만 시뮬레이터 노드가 시작되었습니다!')
        self.get_logger().info('=========================================')
        
        # 주기적으로 사용자 입력을 받아 계산하는 함수를 실행합니다.
        self.run_simulator()

    def run_simulator(self):
        W_BASE = 1.4
        TREAD = 0.42
        
        while rclpy.ok():  # ROS 2 시스템이 정상 작동하는 동안 무한 반복
            user_input = input("\n원하는 조향각을 입력하세요 (-45 ~ 45도, 종료: q): ")
            
            if user_input.lower() == 'q':
                self.get_logger().info("시뮬레이터를 종료합니다.")
                break
                
            try:
                angle = float(user_input)
                if angle < -45 or angle > 45:
                    print("[경고] 조향 물리 한계를 벗어났습니다!")
                    continue
                    
                in_angle, out_angle = calculate_ackermann(angle, W_BASE, TREAD)
                
                print(f"--> 입력 조향각: {angle}°")
                print(f"--> [계산 결과] 안쪽 바퀴 각도: {in_angle:.2f}°")
                print(f"--> [계산 결과] 바깥쪽 바퀴 각도: {out_angle:.2f}°")
                print(f"--> 양쪽 바퀴 조향각 차이: {abs(in_angle - out_angle):.2f}°")
                
            except ValueError:
                print("[오류] 올바른 숫자나 'q'를 입력해주세요.")


# =====================================================================
# [ROS 2 추가분 3] 메인 함수에서 ROS 2를 초기화하고 노드를 실행해 줍니다.
# =====================================================================
def main(args=None):
    # ROS 2 파이썬 통신 시스템 초기화
    rclpy.init(args=args)
    
    # 우리가 만든 시뮬레이터 노드 생성
    node = AckermannSimulatorNode()
    
    # 프로그램이 종료되면 안전하게 자원 해제
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()