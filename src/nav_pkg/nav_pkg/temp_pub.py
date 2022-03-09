import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile # 퍼블리셔의 QoS 설정
from std_msgs.msg import String # 퍼블리시 메시지 타입


class HelloworldPublisher(Node): # Node 클래스 상속

    def __init__(self):
        super().__init__('helloworld_publisher') # 노드 이름 지정
        qos_profile = QoSProfile(depth=10) # 퍼블리시할 데이터를 버퍼에 10개까지 저장
        self.helloworld_publisher = self.create_publisher(String, 'nav_arrive', qos_profile)
				# 퍼블리셔 설정 : 토픽 메시지 타입, 이름, QoS 설정
        self.timer = self.create_timer(1, self.publish_helloworld_msg)
				# 콜백함수 : n초마다 지정한 콜백함수 실행
        self.count = 0

    def publish_helloworld_msg(self):
        msg = String() # 퍼블리시할 메시지
        msg.data = 'temp 도착: {0}'.format(self.count) # 메시지 저장
        self.helloworld_publisher.publish(msg) # 메시지 퍼블리시
        self.get_logger().info('Published message: {0}'.format(msg.data)) # 콘솔창에 출력 (==print함수)
        # logger 종류 : debug, info, warning, error, fatal
        self.count += 1


def main(args=None):
    rclpy.init(args=args) # 초기화
    node = HelloworldPublisher()
    try:
        rclpy.spin(node) # 콜백함수 실행
    except KeyboardInterrupt: # 'Ctrl+c'와 같은 인터럽트 시그널 예외 상황
        node.get_logger().info('Keyboard Interrupt (SIGINT)')
    finally:
        node.destroy_node() # 노드 소멸
        rclpy.shutdown() # 함수 종료


if __name__ == '__main__':
    main()
