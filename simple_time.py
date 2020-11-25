from cv2 import cv2
from  marker_reader import MarkerReader



class Player:

    def __init__(self, filename: str, markersFilename: str):
        self.filename = filename
        self.presentationName = "Presentazione"

        cap = cv2.VideoCapture(self.filename)
        self.fps = int(cap.get(5))
        self.markers = MarkerReader(self.fps, markersFilename, int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
        self.markerList = self.markers.markers
        self.numMarkers = self.markers.numMarkers
        self.markerIndex = 0
        self.fullScreen = False

        self.width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        cap.release()
        cv2.namedWindow(self.presentationName, cv2.WND_PROP_FULLSCREEN)

    def set_unset_full_screen(self):
        if not self.fullScreen:
            cv2.setWindowProperty(self.presentationName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            self.fullScreen = True
        else:
            cv2.setWindowProperty(self.presentationName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
            self.fullScreen = False

    def set_frame(self, cap, marker_index):
        if cap is not None:
            cap.release()
        cap = cv2.VideoCapture(self.filename)
        frame_num = self.markerList[marker_index] if marker_index != self.numMarkers-1 \
            else self.markerList[marker_index]-1
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = cap.read()
        cv2.imshow(self.presentationName, frame)
        return cap

    @staticmethod
    def quit(cap):
        cap.release()
        cv2.destroyAllWindows()

    def play(self, cap, marker_index):
        if cap is not None:
            cap.release()
        cap = cv2.VideoCapture(self.filename)
        cap.set(cv2.CAP_PROP_POS_FRAMES, self.markerList[marker_index])
        i = self.markerList[marker_index]

        while cap.isOpened() and i < self.markerList[marker_index + 1]:
            ret, frame = cap.read()
            cv2.waitKey(self.fps)
            if ret:
                cv2.imshow(self.presentationName, frame)
            else:
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            i += 1
        return cap

    def start_presentation(self):

        end_presentation = False
        cap = self.set_frame(None, 0)
        while not end_presentation:
            key = cv2.waitKey()
            if key == ord(' '):
                if self.markerIndex < self.numMarkers - 1:
                    cap = self.play(cap, self.markerIndex)
                    self.markerIndex += 1
                else:
                    if self.markerIndex == self.numMarkers - 1:
                        cap = self.set_frame(cap, self.markerIndex)
                        self.markerIndex += 1

            else:
                if key == 83:
                    if self.markerIndex < self.numMarkers - 1:
                        self.markerIndex += 1
                        cap = self.set_frame(cap, self.markerIndex)

                if key == 81:
                    if self.markerIndex > 0:
                        self.markerIndex -= 1
                        cap = self.set_frame(cap, self.markerIndex)

                if key == 27:
                    self.quit(cap)
                    end_presentation = True

                if key == ord('f'):
                    self.set_unset_full_screen()



presentation = Player("../test presentazione.mp4", '../test presentazione.csv')
presentation.start_presentation()
