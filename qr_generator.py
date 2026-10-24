import os
import qrcode
from PIL import Image

QR_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "qr_codes")

def ensure_qr_dir():
    if not os.path.exists(QR_DIR):
        os.makedirs(QR_DIR, exist_ok=True)

def generate_product_qr(product_id, verification_url=None):
    """Generates a high-quality QR code for the product ID or verification URL."""
    ensure_qr_dir()
    
    # Payload can be verification URL or the raw product ID
    payload = verification_url if verification_url else product_id

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(payload)
    qr.make(fit=True)

    img = qr.make_image(fill_color="#0f172a", back_color="#ffffff")
    
    # Sanitize file name
    safe_filename = "".join([c if c.isalnum() or c in ('-', '_') else '_' for c in product_id]) + ".png"
    filepath = os.path.join(QR_DIR, safe_filename)
    img.save(filepath)

    return f"/static/qr_codes/{safe_filename}"
