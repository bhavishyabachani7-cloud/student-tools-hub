from flask import Flask, render_template, request, send_file
from PIL import Image
from fpdf import FPDF
import io
import os

app = Flask(__name__)

# ---------- BMI Calculator ----------
@app.route('/bmi', methods=['POST'])
def bmi():
    weight = float(request.form.get('weight', 0))
    height = float(request.form.get('height', 0))
    if height == 0:
        result = "Height cannot be zero!"
    else:
        bmi_value = weight / ((height / 100) ** 2)
        result = f"Your BMI is: {bmi_value:.2f}"
    return render_template('index.html', tool="bmi", result=result)

# ---------- Discount Calculator ----------
@app.route('/discount', methods=['POST'])
def discount():
    price = float(request.form.get('price', 0))
    discount = float(request.form.get('discount', 0))
    final_price = price - (price * discount / 100)
    result = f"Discounted Price: {final_price:.2f}"
    return render_template('index.html', tool="discount", result=result)

# ---------- Word Counter ----------
@app.route('/wordcount', methods=['POST'])
def wordcount():
    text = request.form.get('text', "")
    words = len(text.split())
    result = f"Word Count: {words}"
    return render_template('index.html', tool="wordcount", result=result)

# ---------- Image Resizer ----------
@app.route('/resizer', methods=['POST'])
def resizer():
    file = request.files['image']
    width = int(request.form.get('width', 100))
    height = int(request.form.get('height', 100))
    img = Image.open(file)
    img = img.resize((width, height))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return send_file(buf, mimetype='image/png', download_name='resized_image.png', as_attachment=True)

# ---------- Image to PDF ----------
@app.route('/imgtopdf', methods=['POST'])
def imgtopdf():
    file = request.files['image']
    img = Image.open(file)
    pdf = FPDF()
    pdf.add_page()
    pdf.image(file.stream, x=10, y=10, w=190)
    buf = io.BytesIO()
    pdf.output(buf)
    buf.seek(0)
    return send_file(buf, mimetype='application/pdf', download_name='converted.pdf', as_attachment=True)

# ---------- Image Compressor ----------
@app.route('/imgcompress', methods=['POST'])
def imgcompress():
    file = request.files['image']
    quality = int(request.form.get('quality', 70))
    img = Image.open(file)
    buf = io.BytesIO()
    img.save(buf, format='JPEG', quality=quality)
    buf.seek(0)
    return send_file(buf, mimetype='image/jpeg', download_name='compressed.jpg', as_attachment=True)

# ---------- PDF to Text ----------
@app.route('/pdftotext', methods=['POST'])
def pdftotext():
    import PyPDF2
    file = request.files['pdf']
    try:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        result = text if text.strip() != "" else "No text found."
    except Exception as e:
        result = f"Error reading PDF: {e}"
    return render_template('index.html', tool="pdftotext", result=result)

# ---------- Notes Formatter ----------
@app.route('/notes', methods=['POST'])
def notes():
    content = request.form.get('content', "")
    lines = content.splitlines()
    formatted = ""
    for i, line in enumerate(lines, 1):
        formatted += f"{i}. {line.strip()}\n"
    result = formatted
    return render_template('index.html', tool="notes", result=result)

# ---------- AI Bio Generator ----------
@app.route('/aibio', methods=['POST'])
def aibio():
    name = request.form.get('name', "User")
    profession = request.form.get('profession', "")
    hobbies = request.form.get('hobbies', "")
    bio = f"{name} is a talented {profession}. Loves {hobbies} and is passionate about learning new skills."
    return render_template('index.html', tool="aibio", result=bio)

# ---------- Resume Builder ----------
@app.route('/resume', methods=['POST'])
def resume():
    name = request.form.get('name', "")
    email = request.form.get('email', "")
    phone = request.form.get('phone', "")
    education = request.form.get('education', "")
    experience = request.form.get('experience', "")
    skills = request.form.get('skills', "")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, name, ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Email: {email} | Phone: {phone}", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Education", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 8, education)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Experience", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 8, experience)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Skills", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 8, skills)

    buf = io.BytesIO()
    pdf.output(buf)
    buf.seek(0)
    return send_file(buf, mimetype='application/pdf', download_name='resume.pdf', as_attachment=True)

# ---------- Home Route ----------
@app.route('/')
def home():
    return render_template('index.html', tool="bmi")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)