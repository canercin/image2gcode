import cv2
import numpy as np

def generate_gcode_from_image(image_path, output_path="output_chatgpt1.gcode", scale=1.0):
    # Resmi yükle ve gri tonlamaya çevir
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    height, width = image.shape
    _, binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)

    # Konturları bul
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # G-kod dosyasını oluştur ve başlangıç komutlarını yaz
    with open(output_path, "w") as gcode_file:
        gcode_file.write("G21 ; Set units to millimeters\n")
        gcode_file.write("G90 ; Absolute positioning\n")
        gcode_file.write("G28 ; Home all axes\n")
        gcode_file.write("G1 Z5.0 F500 ; Lift pen\n")

        for contour in contours:
            # İlk kontur noktasına git ve kalemi indir
            x, y = contour[0][0]
            x *= scale
            y = (height - y) * scale  # Y eksenini ters çeviriyoruz
            gcode_file.write(f"G1 X{x:.2f} Y{y:.2f} F1500 ; Move to start of contour\n")
            gcode_file.write("G1 Z0.0 F500 ; Lower pen\n")

            # Kontur noktalarını takip ederek çizim yap
            for point in contour:
                x, y = point[0]
                x *= scale
                y = (height - y) * scale  # Y eksenini ters çeviriyoruz
                gcode_file.write(f"G1 X{x:.2f} Y{y:.2f} F1500\n")

            # Kontur bittiğinde kalemi kaldır
            gcode_file.write("G1 Z5.0 F500 ; Lift pen\n")

        # İşlem bitti, kalemi yukarıda tut ve bitir
        gcode_file.write("G1 Z5.0 F500 ; Lift pen\n")
        gcode_file.write("M84 ; Disable motors\n")

# Resimden G-kod üret
generate_gcode_from_image("pxtest.jpg")

