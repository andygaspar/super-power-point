from cv2 import cv2
import glob



class Player:

    def __init__(self):
        self.files = sorted(glob.glob("../test_presentazione/*.mp4"))
        self.numVideos = len(self.files)
        self.presentationName = "Presentazione"
        self.index = 0
        self.fullScreen = False
        cap = cv2.VideoCapture(self.files[0])
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

    def set_initial_frame(self, filename, cap):
        if cap is not None:
            cap.release()
        cap = cv2.VideoCapture(filename)
        ret, frame = cap.read()
        cv2.imshow(self.presentationName, frame)
        return cap

    @staticmethod
    def quit(cap):
        cap.release()
        cv2.destroyAllWindows()

    def play(self, filename, cap):
        if cap is not None:
            cap.release()
        cap = cv2.VideoCapture(filename)
        fps = cap.get((5))
        while cap.isOpened():
            ret, frame = cap.read()
            cv2.waitKey(int(fps))
            if ret:
                cv2.imshow(self.presentationName, frame)
            else:
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        return cap

    def start_presentation(self):

        end_presentation = False
        file_name = self.files[0]
        cap = self.set_initial_frame(file_name, None)
        while not end_presentation:
            key = cv2.waitKey()
            if key == ord(' '):
                if self.index < self.numVideos - 1:
                    cap = self.play(file_name, cap)
                    self.index += 1
                    file_name = self.files[self.index]
                else:
                    if self.index == self.numVideos - 1:
                        cap = self.play(file_name, cap)
                        self.index += 1
                    else:
                        pass



            else:
                if key == 83:
                    if self.index < self.numVideos - 1:
                        self.index += 1
                        file_name = self.files[self.index]
                        cap = self.set_initial_frame(file_name, cap)

                if key == 81:
                    if self.index > 0:
                        self.index -= 1
                        file_name = self.files[self.index]
                        cap = self.set_initial_frame(file_name, cap)

                if key == 27:
                    self.quit(cap)
                    end_presentation = True

                if key == ord('f'):
                    self.set_unset_full_screen()



presentation = Player()
presentation.start_presentation()
