from ultralytics import YOLO

# load models
yolov8_model = YOLO('./models/yolo11n.pt')
license_plate_detector = YOLO('./models/license_plate_detector.pt')
license_plate_motorbike_detector = YOLO('./models/license_plate_motorbike_detector.pt')
license_plate_character_detector = YOLO('./models/license_plate_character_detector.pt')

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
    # detect vehicles
    detected_vehicles = []
    vehicles = yolov8_model(image)[0]
    for vehicle in vehicles.boxes.data.tolist():
        if int(vehicle[5]) in vehicle_type:
            detected_vehicles.append(vehicle)

    # return if there is no vehicle
    if len(detected_vehicles) == 0:
        return None
    
    # find biggest vehicle on image
    detected_vehicle = max(detected_vehicles, key=lambda x: (x[0] - x[2])*(x[1] - x[3]))

    return detected_vehicle

def detect_license_plates(image, class_id):
    # detect license plate
    detected_license_plates = []

    # motorbike 
    if class_id == 3:
        license_plates = license_plate_motorbike_detector(image)[0]
        detected_license_plates = license_plates.boxes.data.tolist()
    
    # cars, truck, bus
    else:
        license_plates = license_plate_detector(image)[0]
        detected_license_plates = license_plates.boxes.data.tolist()

    # return if there is no licence plate
    if len(detected_license_plates) == 0:
        return None

    # confidence below 0.65 get nuked 
    detected_license_plates_confidence = []
    for data in detected_license_plates:
        if data[4] >= 0.65:
            detected_license_plates_confidence.append(data)
    if len(detected_license_plates_confidence) == 0:
        return None 

    # find biggest license plate on image
    detected_license_plate = max(detected_license_plates_confidence, key=lambda x: (x[0] - x[2])*(x[1] - x[3]))

    return detected_license_plate

def detect_characters(image):
    license_plate_characters = license_plate_character_detector(image)[0]
    data_array = license_plate_characters.boxes.data.tolist()

    # return if there is no character
    if len(data_array) == 0:
        return None

    # sort the data from left to right
    data_array_sorted = sorted(data_array, key=lambda x: x[0])

    # confidence below 0.4 get nuked 
    data_array_confidence = []
    for data in data_array_sorted:
        if data[4] >= 0.4:
            data_array_confidence.append(data)
    if len(data_array_confidence) < 2:
        return None

    # take class data from sorted array
    class_array = [row[5] for row in data_array_confidence]

    # convert class data to character
    character_array = [class_dictionary.get(key, None) for key in class_array]

    # convert character array into string 
    character_string = ''.join(character_array)
    return character_string