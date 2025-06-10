import numpy as np
from ultralytics import YOLO

# load models
yolov8_model = YOLO('./models/yolo11n.pt')
license_plate_detector = YOLO('./models/license_plate_detector_v2.pt')
license_plate_motorbike_detector = YOLO('./models/license_plate_motorbike_detector.pt')
# license_plate_character_detector = YOLO('./models/license_plate_character_detector_v3.pt')
license_plate_character_detector = YOLO('./models/license_plate_character_detector_v3.pt')

# vehicle type {cars, motorbike, bus, truck}
vehicle_type = [2, 3, 5, 7]

# character dictionary
class_dictionary = {0: '0',
                    1: '1',
                    2: '2',
                    3: '3',
                    4: '4',
                    5: '5',
                    6: '6',
                    7: '7',
                    8: '8',
                    9: '9',
                    10: 'A',
                    11: 'B',
                    12: 'C',
                    13: 'D',
                    14: 'E',
                    15: 'F',
                    16: 'G',
                    17: 'H',
                    18: 'I',
                    19: 'J',
                    20: 'K',
                    21: 'L',
                    22: 'M',
                    23: 'N',
                    24: 'O',
                    25: 'P',
                    26: 'Q',
                    27: 'R',
                    28: 'S',
                    29: 'T',
                    30: 'U',
                    31: 'V',
                    32: 'W',
                    33: 'X',
                    34: 'Y',
                    35: 'Z'}

def detect_vehicles(image):
    # detect object
    vehicles = yolov8_model(image)[0]
    detected_vehicles = np.array(vehicles.boxes.data.tolist())
    if detected_vehicles.shape[0] == 0:
        return np.array([])    

    # filter only vehicle
    class_filter = np.isin(detected_vehicles[:, 5], vehicle_type)
    detected_vehicles = detected_vehicles[class_filter]
    if detected_vehicles.shape[0] == 0:
        return np.array([])

    # find biggest vehicle on image
    areas = (detected_vehicles[:, 2] - detected_vehicles[:, 0])*(detected_vehicles[:, 3] - detected_vehicles[:, 1])
    largest_filter = np.argmax(areas)
    detected_vehicle = detected_vehicles[largest_filter]
    
    return detected_vehicle

def detect_license_plates(image, class_id):
    # detect license plate
    detected_license_plates = np.array([])

    # motorbike 
    if class_id == 3:
        license_plates = license_plate_motorbike_detector(image)[0]
        detected_license_plates = np.array(license_plates.boxes.data.tolist())
    
    # cars, truck, bus
    else:
        license_plates = license_plate_detector(image)[0]
        detected_license_plates = np.array(license_plates.boxes.data.tolist())

    if detected_license_plates.shape[0] == 0:
        return np.array([])
    
    # confidence below 0.5 get nuked 
    confidence_filter = detected_license_plates[:, 4] > 0.5
    detected_license_plates = detected_license_plates[confidence_filter]
    if detected_license_plates.shape[0] == 0:
        return np.array([])

    # find highest confidence detected license plate
    largest_confidence_filter = np.argmax(detected_license_plates[:, 4])
    detected_license_plate = detected_license_plates[largest_confidence_filter]

    return detected_license_plate

def detect_characters(image):
    # detect characters
    license_plate_characters = license_plate_character_detector(image)[0]
    detected_characters = np.array(license_plate_characters.boxes.data.tolist())
    if detected_characters.shape[0] == 0:
        return np.array([])
    
    # sort the data from left to right
    detected_characters = detected_characters[detected_characters[:, 0].argsort()]

    # confidence below 0.3 get nuked 
    confidence_filter = detected_characters[:, 4] > 0.3
    detected_characters = detected_characters[confidence_filter]
    if detected_characters.shape[0] == 0:
        return np.array([])

    # # removed double detection
    detected_characters = removed_double_detection(detected_characters)
    if detected_characters.shape[0] < 2:
        return np.array([])

    # take class data from sorted array
    class_array = detected_characters[:, 5]

    # # convert class data to character
    character_array = [class_dictionary.get(key, None) for key in class_array.tolist()]

    # # convert character array into string 
    character_string = ''.join(character_array)
    return character_string

def removed_double_detection(detected_characters):
    filter_arr = []
    x1_temp = 0

    for i, data in enumerate(detected_characters):
        if data[0] < 2:
            filter_arr.append(False)
        elif data[0] - x1_temp < 1:
            if data[4] > detected_characters[i-1][4]:
                filter_arr.pop()
                filter_arr.append(False)
                filter_arr.append(True)
            else:
                filter_arr.append(False)
        else:
            filter_arr.append(True)
            x1_temp = data[0]

    detected_characters = detected_characters[filter_arr]
    return detected_characters