# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 21:54:14 2021

@author: Andro
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
from random import random, randint, seed
import json
seed(1)

class DetVis:
        
    def __init__(self, classes_dict):
        self.orginal_images = []
        self.images = []
        self.labels = {}
        self.classes_dict = classes_dict
        self.colors = {}
        
    def __bb_iou(self, boxA, boxB):
        xA = max(boxA[0], boxB[0])
        yA = max(boxA[1], boxB[1])
        xB = min(boxA[2], boxB[2])
        yB = min(boxA[3], boxB[3])
        interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
        boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
        boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
        iou = interArea / float(boxAArea + boxBArea - interArea)
        return iou
    
    def __cacl_iou(self, det_box, gts, width, height):
        ious = []
        for gt in gts:
            gt = gt.split()
            top_left = (int((float(gt[1]) - float(gt[3])/2) * width), int((float(gt[2]) - float(gt[4])/2) * height))
            bottom_right = (int((float(gt[1]) + float(gt[3])/2) * width), int((float(gt[2]) + float(gt[4])/2) * height))
            gt_box = [top_left[0],top_left[1],bottom_right[0],bottom_right[1]]
            iou = self.__bb_iou(det_box, gt_box)
            if iou > 0:
                ious.append(iou)
        return ious

    def __draw_text_with_background(self, image, text, color, coords, h=50):
        x, y = coords[0], coords[1]
        w = len(text) * 18
        cv2.rectangle(image, (x, y), (x + w, y - h), (0,0,0), -1)
        cv2.putText(image, text, (x + int(w/18),y - int(h/3)), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 4)
        
    def load_images(self, dir_path):
        images_files = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
        for file_name in images_files:
            image_data = {}
            image_data['img'] = cv2.cvtColor(cv2.imread(dir_path + '/' + file_name,cv2.COLOR_BGR2RGB),cv2.COLOR_BGR2RGB)
            image_data['h'] = image_data['img'].shape[0]
            image_data['w'] = image_data['img'].shape[1]
            image_data['name'] = file_name.split('.')[0]
            self.images.append(image_data)
            self.orginal_images.append(image_data)
            
    def load_detections(self, dir_path, detections_format, detections_name):
        single_labels = {}
        single_labels["name"] = detections_name
        single_labels["format"] = detections_format
        labels_files_content = {}
        if single_labels["format"] == "coco":
            file = open(dir_path, 'r')
            detections = json.load(file)
            for detection in detections:
                img_key = detection['image_id'].split('.')[0]
                if img_key not in labels_files_content:
                    labels_files_content[detection['image_id'].split('.')[0]] = []
                det_line = [str(detection['category_id']), str(detection['score'])]
                det_line = det_line + [str(i) for i in detection['bbox']]
                labels_files_content[detection['image_id'].split('.')[0]].append(" ".join(det_line))
            single_labels["detections"] = labels_files_content
        elif single_labels["format"] == "pascal":
            raise ValueError("Pascal format not prepared yet!")
        else:
            labels_files = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
            for file_name in labels_files:
                file = open(dir_path + '\\' + file_name, 'r')
                labels_files_content[file_name.split('.')[0]] = file.readlines()
            single_labels["detections"] = labels_files_content
        self.labels[detections_name] = single_labels
        
    def load_gt(self, dir_path, gt_format):
        self.load_detections(dir_path, gt_format, "GT")
    
    # Convert detections to universal format: class, confidence, top-left, bottom-roght
    def __dets_to_universal_format(self, det_format, det, img):
        detection = {}
        if det_format == "darknet":
            detection['class'] = int(det[0])
            detection['confidence'] = round(float(det[1]),3)
            detection['top_left'] = (int((float(det[2]) - float(det[4])/2) * img['w']), int((float(det[3]) - float(det[5])/2) * img['h']))
            detection['bottom_right'] = (int((float(det[2]) + float(det[4])/2) * img['w']), int((float(det[3]) + float(det[5])/2) * img['h']))
        elif det_format == "detectron":
            detection['class'] = int(det[0])
            detection['confidence'] = round(float(det[1]),3)
            detection['top_left'] = (int((float(det[2]))), int(float(det[3])))
            detection['bottom_right'] = (int((float(det[4]))), int(float(det[5])))
        elif det_format == "coco":
            detection['class'] = int(det[0])
            detection['confidence'] = round(float(det[1]),3)
            detection['top_left'] = (int((float(det[2]))), int((float(det[3]))))
            detection['bottom_right'] = (int((float(det[2]) + float(det[4]))), int((float(det[3]) + float(det[5]))))
        else:
            raise TypeError("Unknown detections format!")
        return detection


            
    def plot_detections(self, detections_name, thickness=4, colors = [], conf_thresh = 0, no_labels = False, iou_calc = False):
        # Rand colors if user does not pass them
        if len(colors) == 0:
            for x in range(len(self.classes_dict)):
                colors.append((randint(0, 255),randint(0, 255),randint(0, 255)))
        if iou_calc:
            gts = self.labels['GT']['detections']
        for i, img in enumerate(self.images):
            for det in self.labels[detections_name]['detections'][img['name']]:
                det = self.__dets_to_universal_format(self.labels[detections_name]['format'], det.split(), img) 
                if det['confidence'] >= conf_thresh:
                    class_name = str(self.classes_dict[det['class']])
                    class_color = colors[det['class']]
                    img['img'] = cv2.rectangle(img['img'], det['top_left'], det['bottom_right'], class_color, thickness)
                    obj_label = class_name + ' ' + str(det['confidence'])
                    if iou_calc:
                        ious = self.__cacl_iou([det['top_left'][0],det['top_left'][1],det['bottom_right'][0],det['bottom_right'][1]], gts[img['name']], img['w'], img['h'])
                        max_iou = 0
                        if len(ious) > 0:
                            max_iou = max(ious)
                        len_ious = len(ious)
                        obj_label = class_name + ' ' + str(det['confidence']) + ' IoU=' + str(round(max_iou,2)) + ' (' + str(len_ious) + ') '
                        self.__draw_text_with_background(img['img'], obj_label, class_color, det['top_left'])
                    else:
                        if not no_labels:
                            self.__draw_text_with_background(img['img'], obj_label, class_color, det['top_left'])
            self.colors[detections_name] = colors
            self.images[i] = img
    
    def plot_gt(self, color, thickness):
        for i, img in enumerate(self.images):
            for det in self.labels['GT']['detections'][img['name']]:
                det = det.split()
                width, height = img['w'], img['h']
                top_left = (int((float(det[1]) - float(det[3])/2) * width), int((float(det[2]) - float(det[4])/2) * height))
                bottom_right = (int((float(det[1]) + float(det[3])/2) * width), int((float(det[2]) + float(det[4])/2) * height))
                img['img'] = cv2.rectangle(img['img'], top_left, bottom_right, color, thickness)
            self.images[i] = img
            
    def __draw_legend_element(self, image, coords, size, class_name, color):
        x, y = coords[0], coords[1]
        cv2.rectangle(image, (x, y), (int(x + size*2), int(y - size*2)), color, -1)
        text_thickness = 1
        if size >= 10:
            text_thickness = 3
        cv2.putText(image, str(class_name), (int(x + size*3), int(y - size*0.75)), cv2.FONT_HERSHEY_SIMPLEX, size*0.07, color, text_thickness)      
        
    def plot_legend(self):
        for n, img in enumerate(self.images):
            img_width, img_height = img['w'], img['h']
            w = 0.2*img_width 
            h = 0.033*img_height * len(self.classes_dict) * len(self.colors)
            cv2.rectangle(img['img'], (int(0.8*img_width), int(0.05*img_height)), (int(0.8*img_width + w), int(0.05*img_height + h)), (0,0,0), -1)
            i = 1
            for model_name in self.colors:
                for class_item in self.classes_dict:
                    self.__draw_legend_element(img['img'], (int(0.8*img_width+0.01*img_width), int(0.05*img_height + 0.03*img_height * i)), 0.01*img_height, model_name + " " + self.classes_dict[class_item], self.colors[model_name][class_item])
                    i += 1
            
    def clear_images(self):
        self.images = self.orginal_images
        
    def print_images(self):
        for image in self.images:
            plt.figure(figsize=(20,20))
            plt.imshow(image['img'])
            
    def save_images(self, path, surfix=""):
        for image in self.images:
            cv2.imwrite(path + '//' + image['name'] + surfix + '.jpg', cv2.cvtColor(image['img'], cv2.COLOR_RGB2BGR)) 