# encoding:utf-8

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time

subscription_key = "afb79cde133c439ba461c6e564dce535"
endpoint = "https://xpbigbang.cognitiveservices.azure.com/"

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

def printed_text(path):
    '''
    Recognize Printed Text with OCR - local
    This example will extract, using OCR, printed text in an image, then print results line by line.
    '''
    print("===== Detect Printed Text with OCR - local =====")
    # Get an image with printed text
    for file in os.listdir(path):
        try:
            print(file)
            local_image_printed_text_path = os.path.join(path,file)
            local_image_printed_text = open(local_image_printed_text_path, "rb")

            ocr_result_local = computervision_client.recognize_printed_text_in_stream(local_image_printed_text,detect_orientation=False,language='zh-Hans')
            print(ocr_result_local)
            if ocr_result_local.orientation == "NotDetected":
                # time.sleep(2)
                continue
            for region in ocr_result_local.regions:
                for line in region.lines:
                    print("Bounding box: {}".format(line.bounding_box))
                    s = ""
                    for word in line.words:
                        s += word.text + " "
                    print(s)
        except Exception as e:
            print(e)
            time.sleep(10)
            continue

    '''
    END - Recognize Printed Text with OCR - local
    ''' 


if __name__ == '__main__':
    printed_text("book/ocrimg5")

