import cv2
import requests
import threading
import time
from datetime import datetime
from detection import *

GO_BACKEND_URL = 'https://go-auth-service.vercel.app/notification/fetch-data' # Ganti sesuai backend Go Anda

last_license_plate = ""

def process_frame(image):
    try:
        # Deteksi kendaraan
        detected_vehicle = detect_vehicles(image)
        if detected_vehicle.shape[0] != 0:
            x1, y1, x2, y2, score, class_id = detected_vehicle
            vehicle_crop_img = image[int(y1):int(y2), int(x1):int(x2)]
            # cv2.imshow("vehicle_crop_img", vehicle_crop_img)

            # Deteksi plat nomor
            detected_license_plate = detect_license_plates(vehicle_crop_img, class_id)
            if detected_license_plate.shape[0] != 0:
                x1, y1, x2, y2, score, class_id = detected_license_plate
                license_plate_crop_img = vehicle_crop_img[int(y1):int(y2), int(x1):int(x2)]
                # cv2.imshow("license_plate_crop_img", license_plate_crop_img)

                # Deteksi karakter
                detected_character = detect_characters(license_plate_crop_img)
                # print(detected_character)
                global last_license_plate
                if detected_character != last_license_plate:
                    last_license_plate = detected_character
                    print(last_license_plate)
                    threading.Timer(10.0, timer).start()
                    # send(vehicle_crop_img, detected_character)

    except Exception as e:
        print(f"⚠️ Error: {e}")

def send(detected_character):
    try:
        # Waktu pemindaian  
        scanned_datetime = datetime.now().isoformat()

        # Kirim ke backend
        payload = {
            'results': detected_character,
            'scanned_at': scanned_datetime
        }

        response = requests.post(GO_BACKEND_URL, json=payload)

        if response.status_code == 200:
            print(f"✅ Dikirim ke backend: {detected_character} @ {scanned_datetime}")
        else:
            print(f"❌ Gagal kirim: Status {response.status_code}")

    except Exception as e:
        print(f"⚠️ Error: {e}")

def timer():
    global last_license_plate
    last_license_plate = ""

def main():
    cap = cv2.VideoCapture(1)  # Webcam laptop atau USB

    # Set resolusi lebih kecil jika perlu (opsional)
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cap.isOpened():
        print("❌ Tidak bisa membuka kamera.")
        return

    print("📸 Kamera aktif... Tekan 'q' untuk keluar.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Tidak bisa membaca frame.")
            continue

        # (opsional) tampilkan kamera
        cv2.imshow("Live Kamera", frame)

        # Proses deteksi + kirim
        process_frame(frame)

        # Delay untuk hindari spam kirim
        cv2.waitKey(3000)  # tunggu 3 detik sebelum lanjut

        # Keluar dengan menekan 'q'
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# for testing
def main_test():
    image = cv2.imread('./image/imagetest16.jpg')
    # cv2.imshow("image", image)

    process_frame(image)

if __name__ == "__main__":
    main()
