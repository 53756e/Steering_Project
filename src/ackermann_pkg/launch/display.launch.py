import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    pkg_name = 'ackermann_pkg'
    
    # URDF 파일 경로 찾기
    urdf_path = os.path.join(
        get_package_share_directory(pkg_name),
        'urdf',
        'ackermann_car.urdf'
    )

    # URDF 파일 읽기
    with open(urdf_path, 'r') as infp:
        robot_desc = infp.read()

    return LaunchDescription([
        # 1. 자동차 뼈대를 인식하고 관절 상태를 뿌려주는 필수 노드
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_desc}]
        ),
        # 2. 3D 시각화 도구 RViz2 실행
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen'
        )
    ])