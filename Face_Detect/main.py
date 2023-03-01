import os
import cv2
from pathlib import Path
from retinaface import RetinaFace
from pprint import pprint
from deepface import DeepFace
import pandas as pd
from deepface.basemodels import VGGFace


def detect_faces(img_path: str, bounding_box: bool = False):
    resp = {}
    obj = RetinaFace.detect_faces(img_path)
    resp["faces"] = obj

    if bounding_box:
        img = cv2.imread(img_path)
        for key in obj.keys():
            identity = obj[key]
            facial_area = identity["facial_area"]
            cv2.rectangle(img, (facial_area[2], facial_area[3]), (facial_area[0], facial_area[1]), (255, 255, 255), 1)
        resp["image"] = img

    return resp


def extract_faces(image_path: str, obj: dict, save_images: bool = False, save_path: str = None):
    resp = {}
    img = cv2.imread(image_path)
    if save_path[-4:] == ".jpg":
        save_path = save_path[:-4]
    for key in obj.keys():
        identity = obj[key]
        facial_area = identity["facial_area"]
        cropped_img = img[facial_area[1]: facial_area[3], facial_area[0]: facial_area[2]]
        resp[key] = cropped_img
        if save_images:
            cv2.imwrite(f'{save_path}_{key}.jpg', cropped_img)
    return resp


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = str(Path(current_dir) / Path("test.jpg"))

    a = detect_faces(image_path, bounding_box=True)
    cv2.imwrite("output.jpg", a["image"])

    b = extract_faces(image_path, a["faces"], save_images=True, save_path=current_dir)


def create_dirtree_without_files(src_dir_path, dst_dir_path, dest_dir_name: str = None):
    src = os.path.abspath(src_dir_path)
    dst = os.path.join(os.path.abspath(dst_dir_path), dest_dir_name)
    src_prefix = len(src) + len(os.path.sep)
    os.makedirs(os.path.join(dst_dir_path, dest_dir_name), exist_ok=True)

    for root, dirs, files in os.walk(src):
        for dirname in dirs:
            dirpath = os.path.join(dst, root[src_prefix:], dirname)
            os.makedirs(dirpath, exist_ok=True)
    return dst


def crop_database(database_path: str, crop_database_base_path: str, crop_database_dir_name: str):
    dst = create_dirtree_without_files(database_path, crop_database_base_path, crop_database_dir_name)
    for directory in os.listdir(database_path):
        for file in os.listdir(os.path.join(database_path, directory)):
            if file.endswith(".jpg"):
                file_path = os.path.join(database_path, directory, file)
                crop_file_path = os.path.join(dst, directory, file)
                resp = detect_faces(file_path)
                extract_faces(file_path, resp["faces"], save_images=True, save_path=crop_file_path)


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    database = str(Path(current_dir) / Path("Database"))
    cropdatabase = str(Path(current_dir) / Path("Crop_Database"))
    cropped_database = "Crop_Database"
    # crop_database(database, current_dir, cropped_database)

    img1_path = os.path.join(current_dir, "Crop_Database/Narendra_Modi/NM1_face_1.jpg")
    img2_path = os.path.join(current_dir, "Crop_Database/Narendra_Modi/NM2_face_1.jpg")
    img3_path = os.path.join(current_dir, "Crop_Database/Vladimir_Putin/Putin1_face_1.jpg")

    img4_path = os.path.join(current_dir, "Database/Narendra_Modi/NM1.jpg")
    img5_path = os.path.join(current_dir, "Database/Narendra_Modi/NM2.jpg")
    img6_path = os.path.join(current_dir, "Database/Vladimir_Putin/Putin1.jpg")

    # resp = DeepFace.verify(img1_path, img2_path, model_name="Facenet", distance_metric="cosine", enforce_detection=False)
    # pprint(resp)
    # print("\n\n\n\n")
    # resp = DeepFace.verify(img1_path, img3_path, model_name="Facenet", enforce_detection=False)
    # pprint(resp)
    # print("\n\n\n\n")
    # resp = DeepFace.verify(img4_path, img5_path, model_name="Facenet", distance_metric="cosine", detector_backend="retinaface")
    # pprint(resp)
    # print("\n\n\n\n")
    # resp = DeepFace.verify(img4_path, img6_path, model_name="Facenet", detector_backend="retinaface")
    # pprint(resp)
    # modell = VGGFace.loadModel()
    chris_path = os.path.join(current_dir, "chris.jpg")
    resp = DeepFace.find(img_path=chris_path, db_path=database, detector_backend="retinaface", model_name="VGG-Face")
    file = open("output.txt", "w")
    for i in resp:
        # save i as excel
        i.to_csv('file2.csv')
    file.close()

