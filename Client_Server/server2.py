#!/usr/bin/env python

import random
import socket, select
from time import gmtime, strftime

import os
import sys
import coco
import utils
import model as modellib

ROOT_DIR = os.getcwd()
MODEL_DIR = os.path.join(ROOT_DIR, "logs")
COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")
if not os.path.exists(COCO_MODEL_PATH):
    utils.download_trained_weights(COCO_MODEL_PATH)

class InferenceConfig(coco.CocoConfig):
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

config = InferenceConfig()
config.display()

model = modellib.MaskRCNN(
    mode="inference", model_dir=MODEL_DIR, config=config
)
model.load_weights(COCO_MODEL_PATH, by_name=True)
class_names = [
    'BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane',
    'bus', 'train', 'truck', 'boat', 'traffic light',
    'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird',
    'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
    'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie',
    'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard',
    'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
    'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
    'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
    'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
    'keyboard', 'cell phone', 'microwave', 'oven', 'toaster',
    'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
    'teddy bear', 'hair drier', 'toothbrush'
]

def main():
    imgcounter = 1
    basename = "image%s.png"

    HOST = '127.0.0.1'
    PORT = 6666
    size = 0

    connected_clients_sockets = []

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)

    connected_clients_sockets.append(server_socket)

    while True:

        read_sockets, write_sockets, error_sockets = select.select(connected_clients_sockets, [], [])

        for sock in read_sockets:

            if sock == server_socket:

                sockfd, client_address = server_socket.accept()
                connected_clients_sockets.append(sockfd)

            else:
                try:
                    size = int((sock.recv(4096)).decode())
                    print(size)
                    sock.sendall("1".encode())

                    myfile = open("temp.png", 'wb')
                    data = sock.recv(size)
                    myfile.write(data)
                    myfile.close()

                    #IMAGE MANIPULATION BEGINS HERE
                    imm = cv2.imread("temp.png")
                    imm = cv2.cvtColor(imm, cv2.COLOR_BGR2GRAY)
                    cv2.imwrite("temp_gray.png",imm)
                    #AND ENDS HERE




                    # frame = cv2.imread("temp.png")
                    #
                    # frame = cv2.resize(frame, (480*2, 340*2))
                    #
                    # results = model.detect([frame], verbose=0)
                    # r = results[0]
                    # frame = display_instances(
                    #     frame, r['rois'], r['masks'], r['class_ids'], class_names, r['scores']
                    # )
                    #
                    #
                    #
                    # # cv2.imshow('frame', frame)
                    # #
                    # # if cv2.waitKey(1) & 0xFF == ord('q'):
                    # #     break
                    #
                    # cv2.imwrite("temp.png",frame)
                    #
                    myfile_gray = open("temp.png", 'rb')
                    bytes = myfile_gray.read()
                    print("Size of sending data is %d" % len(bytes))




                    sock.sendall(bytes)
                    sock.shutdown()
                except:
                    sock.close()
                    connected_clients_sockets.remove(sock)
                    continue
    server_socket.close()

def random_colors(N):
    np.random.seed(1)
    colors = [tuple(255 * np.random.rand(3)) for _ in range(N)]
    return colors


def apply_mask(image, mask, color, alpha=0.5):
    """apply mask to image"""
    for n, c in enumerate(color):
        image[:, :, n] = np.where(
            mask == 1,
            image[:, :, n] * (1 - alpha) + alpha * c,
            image[:, :, n]
        )
    return image


def display_instances(image, boxes, masks, ids, names, scores):
    """
        take the image and results and apply the mask, box, and Label
    """
    n_instances = boxes.shape[0]
    colors = random_colors(n_instances)

    if not n_instances:
        print('NO INSTANCES TO DISPLAY')
    else:
        assert boxes.shape[0] == masks.shape[-1] == ids.shape[0]

    for i, color in enumerate(colors):
        if not np.any(boxes[i]):
            continue
    #
        y1, x1, y2, x2 = boxes[i]
        label = names[ids[i]]
        score = scores[i] if scores is not None else None
        caption = '{} {:.2f}'.format(label, score) if score else label
        mask = masks[:, :, i]


        # print(label, " + ", color)

        if(label == 'person'):
            color = (255,0,0) # Blue
        else:
            if(score.item() > 0.9):
                color = (0,255,0) # Green
            else:
                color = (0,0,255) # Red

        image = apply_mask(image, mask, color)
        image = cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        image = cv2.putText(
            image, caption, (x1, y1), cv2.FONT_HERSHEY_COMPLEX, 0.7, color, 2
        )

    return image



main()
