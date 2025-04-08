import cv2
from pyzbar.pyzbar import decode
import logging
import numpy as np

logger = logging.getLogger(__name__)

def read_barcode(image_data):
    try:
        # Convertir imagen a formato OpenCV
        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Decodificar códigos de barras
        detected_barcodes = decode(img)
        
        if not detected_barcodes:
            logger.warning("No se detectaron códigos de barras")
            return None

        results = []
        for barcode in detected_barcodes:
            barcode_data = {
                'data': barcode.data.decode('utf-8'),
                'type': barcode.type,
                'rect': barcode.rect,
                'quality': barcode.quality
            }
            results.append(barcode_data)
            logger.info(f"Código detectado: {barcode_data}")

        return results

    except Exception as e:
        logger.error(f"Error leyendo código de barras: {str(e)}")
        return None

def validate_barcode(barcode):
    # Validación básica de código de barras (EAN-13)
    if len(barcode) != 13:
        return False
    try:
        int(barcode)
        return True
    except ValueError:
        return False