import cv2
from datetime import datetime
import requests
from detection import *

GO_BACKEND_URL = 'http://localhost:3100/notification/fetch-data'  # Ganti sesuai backend Go Anda

def process_frame(frame):
    try:
        # Deteksi kendaraan
        detected_vehicle = detect_vehicles(frame)
        if detected_vehicle != None:
            x1, y1, x2, y2, score, class_id = detected_vehicle
            vehicle_crop_img = frame[int(y1):int(y2), int(x1):int(x2)]

            # Deteksi plat nomor
            detected_license_plate = detect_license_plates(vehicle_crop_img, class_id)
            if detected_license_plate != None:
                x1, y1, x2, y2, score, class_id = detected_license_plate
                license_plate_crop_img = vehicle_crop_img[int(y1):int(y2), int(x1):int(x2)]

                # Deteksi karakter
                detected_character = detect_characters(license_plate_crop_img)
                print(detected_character)
                # if detected_character != None:                    
                #     # Waktu pemindaian  
                #     scanned_datetime = datetime.now().isoformat()

                #     # Kirim ke backend
                #     payload = {
                #         'results': detected_character,
                #         'scanned_at': scanned_datetime
                #     }

                #     response = requests.post(GO_BACKEND_URL, json=payload)

                #     if response.status_code == 200:
                #         print(f"✅ Dikirim ke backend: {detected_character} @ {scanned_datetime}")
                #     else:
                #         print(f"❌ Gagal kirim: Status {response.status_code}")

    except Exception as e:
        print(f"⚠️ Error saat proses frame: {e}")
        

def main():
    # image = cv2.imread('./image/imagetest6.jpg')
    # # cv2.imshow("image", image)

    # process_frame(image)

    cap = cv2.VideoCapture(0)  # Webcam laptop atau USB

    # Set resolusi lebih kecil jika perlu (opsional)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

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
        # cv2.waitKey(1000)  # tunggu 5 detik sebelum lanjut

        # Keluar dengan menekan 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
