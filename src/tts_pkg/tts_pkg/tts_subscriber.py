import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from std_msgs.msg import String


class TTS_Subscriber(Node):

    def __init__(self):
        super().__init__('TTS_Subscriber') # Node 클래스 생성자 호출
        qos_profile = QoSProfile(depth=10) # 서브스크라이브 데이터를 버퍼에 10개까지 저장

        # OCR -> TTS
        self.tts_subscriber = self.create_subscription(
            String, # 토픽 메시지 타입
            'ocr_message', # 토픽 이름
            self.ocr_message_detect, # 콜백 함수
            qos_profile) # QoS 설정

        # nav -> TTS
        self.tts_subscriber = self.create_subscription(
            String, # 토픽 메시지 타입
            'nav_arrive', # 토픽 이름
            self.nav_message, # 콜백 함수
            qos_profile) # QoS 설정

        # FACE_DETECTION -> TTS
        self.face_subscriber = self.create_subscription(
            String, # 토픽 메시지 타입
            'face_detection_result', # 토픽 이름
            self.face_message_detect, # 콜백 함수
            qos_profile) # QoS 설정


    # OCR
    def ocr_message_detect(self, msg) :
        TF = True
        message = msg.data
        if message == "" & TF == True:
            msg_to_tts("다시 촬영해주세요.")
            TF = False
        else :
            msg_to_tts(message)

    # NAV
    def nav_message(self, msg) :
        TF = True
        msg_to_tts("도착하였습니다.")
        TF = False


    # FACE_DETECTION
    def face_message_detect(self, msg_pub) :
        print("도착했나?")
        message = msg_pub.data
        print(message)
        TF = True
        if message == "0":
            msg_to_tts("다시 촬영해주세요.")
        else :
            msg_to_tts("조유경님, 저에게 물품을 주세요")
        TF = False


def msg_to_tts(message):

    import os
    import sys
    import urllib.request
    import time
    # import playsound

    client_id = "572137kphp"
    client_secret = "zFYBdm3ECMbRszC3sVagpMdD2rsWkBnnA9cFvuEL"

    encText = urllib.parse.quote(message)

    data = "speaker=nara&volume=0&speed=0&pitch=0&format=mp3&text=" + encText;
    url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"

    request = urllib.request.Request(url)
    request.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
    request.add_header("X-NCP-APIGW-API-KEY",client_secret)

    response = urllib.request.urlopen(request, data=data.encode('utf-8'))
    rescode = response.getcode()

    if response.getcode()==200:
        print("CSS 성공! 파일을 저장합니다.")
        response_body = response.read()
        file_name = "음성파일"
        with open(file_name + ".mp3", 'wb') as f:
            f.write(response_body)
        print("파일명:", file_name)
        # playsound.playsound(file_name+".mp3")
    else:
        print("Error Code:" + rescode)


def main(args=None):
    rclpy.init(args=args)
    node = TTS_Subscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Keyboard Interrupt (SIGINT)')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
