import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile # 퍼블리셔의 QoS 설정
from std_msgs.msg import String # 퍼블리시 메시지 타입


class Nav_Sub_Publisher(Node): # Node 클래스 상속

    def __init__(self):
        super().__init__('Nav_Sub_Publisher') # 노드 이름 지정
        qos_profile = QoSProfile(depth=10) # 퍼블리시할 데이터를 버퍼에 10개까지 저장

        # 도착 정보 sub : ??? -> nav
        self.nav_arrive_subscriber = self.create_subscription(
            String, # 토픽 메시지 타입
            'nav_arrive', # 토픽 이름
            self.nav_subscribe_msg, # 콜백 함수
            qos_profile) # QoS 설정

        # 도착 정보 publish
        self.nav_arrive_publisher = self.create_publisher(String, 'face_start', qos_profile)
        self.timer = self.create_timer(1, self.nav_publisher_msg)
        self.count = 0


    def nav_subscribe_msg(self, msg):
        self.message = msg.data
        self.get_logger().info('Received message: {0}'.format(msg.data))

    def nav_publisher_msg(self):
        msg = String() # 퍼블리시할 메시지
        msg.data = ('도착 {0}'.format(self.count)) # 메시지 저장
        self.nav_arrive_publisher.publish(msg) # 메시지 퍼블리시
        self.get_logger().info('Published message: {0}'.format(msg.data))
        self.count += 1


def main(args=None):
    rclpy.init(args=args) # 초기화
    node = Nav_Sub_Publisher()
    try:
        node.get_logger().info("spin될까?")
        rclpy.spin(node) # 콜백함수 실행
        node.get_logger().info("spin된다!!")

    except KeyboardInterrupt: # 'Ctrl+c'와 같은 인터럽트 시그널 예외 상황
        node.get_logger().info('Keyboard Interrupt (SIGINT)')
    finally:
        node.destroy_node() # 노드 소멸
        rclpy.shutdown() # 함수 종료


if __name__ == '__main__':
    main()
