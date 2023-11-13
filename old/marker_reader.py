import pandas as pd


class MarkerReader:
    def __init__(self, fps, marker_filename, final_frame):
        self.df = pd.read_csv(marker_filename, encoding='utf16', sep="\t")
        self.markers = self.convert_markers(self.df["Attacco"].tolist(), fps)

        if self.markers[0] != 0:
            self.markers = [0] + self.markers
        if self.markers[-1] != final_frame:
            self.markers = self.markers + [final_frame]

        self.numMarkers = len(self.markers)

    @staticmethod
    def convert_markers(markers_time, fps):
        markers_frame = []
        for marker in markers_time:
            markers_frame.append(
                (int(marker[:2]) * 3600 + int(marker[3:5]) * 60 + int(marker[6:8])) * fps + int(marker[9:]))

        return markers_frame


