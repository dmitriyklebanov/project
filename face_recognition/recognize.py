import numpy as np
import cv2

from tensorflow.keras.models import load_model


class FaceRecognition:
    emotion_mapping = {0: 'Angry', 1: 'Disgust', 2: 'Fear', 3: 'Happy', 4: 'Sad', 5: 'Surprise', 6: 'Neutral'}

    def __init__(self):
        self.face_detection_model = cv2.CascadeClassifier('face_recognition/models/face_detection.xml')
        self.emotion_classification_model = load_model('face_recognition/models/emotion_classification.hdf5')

    def view_camera(self, file):
        # ret, image = self.capture.read()
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        print('starting')
        # file = 'happy_face.jpg'
        image = cv2.imread(file)
        image, emotion = self.process_image(image)
        # height, width, channel = image.shape
        print(emotion)
        # step = channel * width
        # qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
        # self.ui.image_label.setPixmap(QPixmap.fromImage(qImg))

    def classify_emotion(self, image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        gray_image = gray_image.astype('float32')
        gray_image /= 255.0

        resized_image = cv2.resize(gray_image, (48, 48), interpolation=cv2.INTER_AREA)
        resized_image.resize((1, 48, 48, 1))
        predict = self.emotion_classification_model.predict(resized_image)

        return self.emotion_mapping[np.argmax(predict)]

    def detect_face(self, image):
        result = self.face_detection_model.detectMultiScale(image, 1.3, 2)
        if len(result):
            return result[0]
        else:
            return None

    def process_image(self, image):
        result = image
        face_bounding_box = self.detect_face(image)

        emotion = None
        if face_bounding_box is not None:
            x, y, w, h = face_bounding_box
            emotion = self.classify_emotion(result[y: y + h, x: x + w])
            cv2.putText(result, emotion, (x + 5, y - 10), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
            cv2.rectangle(result, (x, y), (x + w, y + h), (255, 255, 255), 2)
        return result, emotion


if __name__ == '__main__':
    face_recognition = FaceRecognition()
    face_recognition.view_camera()