from flask import Flask, render_template, jsonify, request
from PIL import Image, ImageOps, ImageEnhance
import random
import io
import base64

app = Flask(__name__)

# Daftar operasi yang dapat diterapkan
operations = ['grayscale', 'flip', 'rotate', 'brightness', 'threshold']

def apply_operation(image, operation):
    """Fungsi untuk menerapkan satu operasi pengolahan citra."""
    if operation == 'grayscale':
        image = ImageOps.grayscale(image)
    elif operation == 'flip':
        image = ImageOps.mirror(image)
    elif operation == 'rotate':
        image = image.rotate(90)
    elif operation == 'brightness':
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(1.5)
    elif operation == 'threshold':
        image = image.convert('L')
        image = image.point(lambda p: p > 128 and 255)
    return image

@app.route('/')
def index():
    """Render halaman game."""
    return render_template('index.html')

@app.route('/get_image', methods=['POST'])
def get_image():
    """Mengirimkan gambar asli dan gambar yang diproses ke frontend."""
    level = int(request.json['level'])
    img_path = 'images/sample.jpg'  # Ganti dengan gambar yang diinginkan
    img = Image.open(img_path)

    if level == 1:
        chosen_ops = [random.choice(operations)]
    else:
        chosen_ops = random.sample(operations, 2)

    processed_img = img.copy()
    for op in chosen_ops:
        processed_img = apply_operation(processed_img, op)

    # Convert images to base64 to send to frontend
    img_before = io.BytesIO()
    img.save(img_before, format="JPEG")
    img_before = base64.b64encode(img_before.getvalue()).decode()

    img_after = io.BytesIO()
    processed_img.save(img_after, format="JPEG")
    img_after = base64.b64encode(img_after.getvalue()).decode()

    return jsonify({
        'before': img_before,
        'after': img_after,
        'operations': chosen_ops  # Ini untuk validasi jawaban
    })

if __name__ == '__main__':
    app.run(debug=True)
