import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile # 퍼블리셔의 QoS 설정
from std_msgs.msg import String # 퍼블리시 메시지 타입

class OCR_Publisher(Node): # Node 클래스 상속

    def __init__(self):
        super().__init__('OCR_Publisher') # 노드 이름 지정
        qos_profile = QoSProfile(depth=10) # 퍼블리시할 데이터를 버퍼에 10개까지 저장
        self.ocr_publisher = self.create_publisher(String, 'ocr_message', qos_profile)
        self.timer = self.create_timer(1, self.publish_msg) # 콜백함수 : n초마다 지정한 콜백함수 실행
        self.count = 0

    def publish_msg(self):
        self.ocr()
        msg = String() # 퍼블리시할 메시지
        msg.data = self.message # 메시지 저장
        self.ocr_publisher.publish(msg) # 메시지 퍼블리시
        self.get_logger().info('Published message: {0}'.format(msg.data)) # 콘솔창에 출력 (==print함수)


    # 운송장 이미지 -> OCR 결과
    def ocr(self) :

        import requests
        import uuid
        import time
        import json

        api_url = 'https://2db3c4f0f443425e91076e90310bc461.apigw.ntruss.com/custom/v1/13111/71345557e5b12d3b42ffdbf516755f0c9c7f7c3bc51dd5cea5d888581fc4d9a7/infer'
        secret_key = 'S3RtbGdXWUtDc0xlYW1ybGFrTGhEanlMWHdpbmRCTHM='

        # 이미지 input 이후
        image_file = 'input.png' # robot_ws 에 위치, 현재 '조유경'
        output_file = 'output.json'

        request_json = {
            'images': [
                {
                    'format': 'jpg',
                    'name': 'demo',
                    'templateIds': [12333]
                }
            ],
            'requestId': str(uuid.uuid4()),
            'version': 'V2',
            'timestamp': int(round(time.time() * 1000))
        }
        payload = {'message': json.dumps(request_json).encode('UTF-8')}
        files = [
            ('file', open(image_file,'rb'))
        ]
        headers = {
            'X-OCR-SECRET': secret_key
        }

        response = requests.request("POST", api_url, headers=headers, data = payload, files = files)

        res = json.loads(response.text.encode('utf8'))

        with open(output_file, 'w', encoding='utf-8') as outfile:
            json.dump(res, outfile, indent=4, ensure_ascii=False)

        # company = res['images'][0]['title']['inferText']
        name = res['images'][0]['fields'][0]['inferText']
        # product = res['images'][0]['fields'][1]['inferText']
        # name = ""
        self.message = name



def main(args=None):
    rclpy.init(args=args) # 초기화
    node = OCR_Publisher()

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
