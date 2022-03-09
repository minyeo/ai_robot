import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile # 퍼블리셔의 QoS 설정
from std_msgs.msg import String # 퍼블리시 메시지 타입

class Face_Start_Sub_Pub(Node): # Node 클래스 상속

    def __init__(self):
        super().__init__('Face_Start_Sub_Pub') # 노드 이름 지정
        qos_profile = QoSProfile(depth=10) # 퍼블리시할 데이터를 버퍼에 10개까지 저장

        # start 신호 subscribe
        self.face_start_subscriber = self.create_subscription(
            String,
            'face_start',
            self.subscribe_topic_message,
            qos_profile)
        # face_detection 결과 publish
        self.face_publisher = self.create_publisher(
            String,
            'face_detection_result',
            qos_profile)
        self.timer = self.create_timer(1, self.publish_topic_message) # 콜백함수 : n초마다 지정한 콜백함수 실행
        self.count = 0

    # start 신호 subscribe
    def subscribe_topic_message(self, msg):
        self.get_logger().info('Received message: {0}'.format(msg.data))
        self.name = msg

    # face_detection 결과 publish
    def publish_topic_message(self):
        msg_pub = String()
        msg_pub.data = face_detection(self.name) # face_detection 결과 : 일치 여부
        self.face_publisher.publish(msg_pub) # 메시지 퍼블리시
        self.get_logger().info('Published message: {0}'.format(msg_pub.data))

    # n초 이상 실행 시
def face_detection(message): # message = name
    """
    import face_recognition
    import cv2
    import numpy as np

    # 통신으로 input_name 받아와야함, 지금은 test로 통신 받는 다는 가정하에 넣어놓음
    input_name=message
    # ros로 넘길 output, 마지막에 통신으로 받은 name과 얼굴인식 match 이면 1, 다르면 0 을 넘김
    true_or_false = 0

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    # window_name=''


    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)

    # Load a sample picture and learn how to recognize it.
    dy_image = face_recognition.load_image_file("dy.png")
    dy_image = cv2.cvtColor(dy_image, cv2.COLOR_BGR2RGB)
    dy_face_encoding = face_recognition.face_encodings(dy_image)[0]

    js_image = face_recognition.load_image_file("js.png")
    js_image = cv2.cvtColor(js_image, cv2.COLOR_BGR2RGB)
    js_face_encoding = face_recognition.face_encodings(js_image)[0]

    yk_image = face_recognition.load_image_file("yk.png")
    yk_image = cv2.cvtColor(yk_image, cv2.COLOR_BGR2RGB)
    yk_face_encoding = face_recognition.face_encodings(yk_image)[0]

    je_image = face_recognition.load_image_file("je.png")
    je_image = cv2.cvtColor(je_image, cv2.COLOR_BGR2RGB)
    je_face_encoding = face_recognition.face_encodings(je_image)[0]

    sb_image = face_recognition.load_image_file("sb.png")
    sb_image = cv2.cvtColor(sb_image, cv2.COLOR_BGR2RGB)
    sb_face_encoding = face_recognition.face_encodings(sb_image)[0]

    my_image = face_recognition.load_image_file("my.png")
    my_image = cv2.cvtColor(my_image, cv2.COLOR_BGR2RGB)
    my_face_encoding = face_recognition.face_encodings(my_image)[0]

    ej_image = face_recognition.load_image_file("ej.png")
    ej_image = cv2.cvtColor(ej_image, cv2.COLOR_BGR2RGB)
    ej_face_encoding = face_recognition.face_encodings(ej_image)[0]

    # Create arrays of known face encodings and their names
    known_face_encodings = [
        dy_face_encoding,
        js_face_encoding,
        yk_face_encoding,
        je_face_encoding,
        sb_face_encoding,
        my_face_encoding,
        ej_face_encoding,
    ]
    known_face_names = [
        "Doyoung",
        "Jinsung",
        "Youkyong",
        "Jieun",
        "Subeen",
        "Minyoung",
        "Eojin",
    ]
    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=.25, fy=.25)


        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (255, 255, 255), 2)

            if input_name == name:
                true_or_false = 1
                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (255, 0, 0), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            else:
                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, 'Not match', (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                true_or_false = 0

        # Display the resulting image
        frame = cv2.resize(frame,(1280,720))
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if true_or_false == 1:
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
    """
    return "1"


def sub_main(args=None):
    rclpy.init(args=args) # 초기화
    node = Face_Start_Sub_Pub()
    try:
        rclpy.spin(node) # 콜백함수 실행
    except KeyboardInterrupt: # 'Ctrl+c'와 같은 인터럽트 시그널 예외 상황
        node.get_logger().info('Keyboard Interrupt (SIGINT)')
    finally:
        node.destroy_node() # 노드 소멸
        rclpy.shutdown() # 함수 종료


if __name__ == '__main__':
    sub_main()
