# import cv2
# from datetime import datetime
# from flask import Flask, request, jsonify
# from detection import *

# app = Flask(__name__)

# @app.route("/notification/fetch-data")
# def get_license_plate():
#     # buka kamera
#     # cap = cv2.VideoCapture(0)

#     # foto kamera
#     # ret, image = cap.read()

#     # tutup kamera
#     # cap.release()

#     # load image from file
#     image = cv2.imread('./image/imagetest16.jpg')
#     # cv2.imshow("image", image)
#     # cv2.waitKey(0)

#     # detecting vehicle
#     detected_vehicle = detect_vehicles(image)
#     x1, y1, x2, y2, score, class_id = detected_vehicle
#     vehicle_crop_img = image[int(y1):int(y2), int(x1): int(x2), :]
#     # cv2.imshow("vehicle_crop_img", vehicle_crop_img)
#     # cv2.waitKey(0)

#     # detecting license plate
#     detected_license_plate = detect_license_plates(vehicle_crop_img, class_id)
#     x1, y1, x2, y2, score, class_id = detected_license_plate
#     license_plate_crop_img = vehicle_crop_img[int(y1):int(y2), int(x1): int(x2), :]
#     cv2.imshow("license_plate_crop_img", license_plate_crop_img)
#     cv2.waitKey(0)

#     # detecting character on license plate
#     detected_character = detect_characters(license_plate_crop_img)

#     # current time
#     scanned_datetime = datetime.now().isoformat()

#     payload = {
#         'results': detected_character,
#         'scanned_at': scanned_datetime
#     }

#     return jsonify(payload), 200

# @app.errorhandler(500)
# def internal_error():
#     return jsonify({'error': 'Internal server error'}), 500

# if __name__ == "__main__":
#     app.run(debug = True)

# import cv2
# import numpy as np
# from datetime import datetime
# import requests
# from detection import *

# GO_BACKEND_URL = 'http://localhost:3100/notification/fetch-data'  # Ganti sesuai backend Go Anda

# def process_frame_and_send(frame):
#     try:
#         # Deteksi kendaraan
#         detected_vehicle = detect_vehicles(frame)
#         x1, y1, x2, y2, score, class_id = detected_vehicle
#         vehicle_crop_img = frame[int(y1):int(y2), int(x1):int(x2)]

#         # Deteksi plat nomor
#         detected_license_plate = detect_license_plates(vehicle_crop_img, class_id)
#         x1, y1, x2, y2, score, class_id = detected_license_plate
#         license_plate_crop_img = vehicle_crop_img[int(y1):int(y2), int(x1):int(x2)]

#         # Deteksi karakter
#         detected_character = detect_characters(license_plate_crop_img)

#         # Waktu pemindaian
#         scanned_datetime = datetime.now().isoformat()

#         # Kirim ke backend
#         payload = {
#             'results': detected_character,
#             'scanned_at': scanned_datetime
#         }

#         response = requests.post(GO_BACKEND_URL, json=payload)

#         if response.status_code == 200:
#             print(f"✅ Dikirim ke backend: {detected_character} @ {scanned_datetime}")
#         else:
#             print(f"❌ Gagal kirim: Status {response.status_code}")

#     except Exception as e:
#         print(f"⚠️ Error saat proses frame: {e}")

# def main():
#     cap = cv2.VideoCapture(0)  # Webcam laptop atau USB

#     # Set resolusi lebih kecil jika perlu (opsional)
#     cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

#     if not cap.isOpened():
#         print("❌ Tidak bisa membuka kamera.")
#         return

#     print("📸 Kamera aktif... Tekan 'q' untuk keluar.")

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             print("⚠️ Tidak bisa membaca frame.")
#             continue

#         # (opsional) tampilkan kamera
#         cv2.imshow("Live Kamera", frame)

#         # Proses deteksi + kirim
#         process_frame_and_send(frame)

#         # Delay untuk hindari spam kirim
#         cv2.waitKey(3000)  # tunggu 3 detik sebelum lanjut

#         # Keluar dengan menekan 'q'
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# if __name__ == "__main__":
#     main()







# # Dapatkan waktu saat ini
# scanned_datetime = datetime.now().isoformat()

# # Kirim hasil ke backend Go
# backend_url = 'http://localhost:3100/notification/fetch-data'  # Ganti dengan URL backend Anda
# try:
#     payload = {
#         'results': detected_character,
#         'scanned_at': scanned_datetime
#     }
#     response = requests.post(backend_url, json=payload)
#     if response.status_code == 200:
#         print("Hasil berhasil dikirim ke backend.")
#     else:
#         print(f"Gagal mengirim hasil ke backend. Status code: {response.status_code}")
# except Exception as e:
#     print(f"Terjadi kesalahan saat mengirim ke backend: {e}")
