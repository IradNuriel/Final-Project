import os



from .faceDataSet import FaceDataSet


class YaleFaceDataSet(FaceDataSet):

    def __init__(self, path, ext_list, n_classes):
        super().__init__(path, ext_list, n_classes)

    def process_label(self, img_path):
        val = int(os.path.split(img_path)[1].split(".")[0].replace("subject", "")) - 1
        if val not in self.labels:
            self.number_labels+=1
        return val
