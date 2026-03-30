from flask import Flask, render_template, request, send_file
from PIL import Image
from fpdf import FPDF
import io
import os
import PyPDF2

app = Flask(__name__)

# ---------- HOME ----------
@app.route('/')
def home():
    return render_template('index.html', tool="bmi", result=None)

# ---------- PAGES ----------
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

# ---------- BMI ----------
@app.route('/bmi', methods=['POST'])
def bmi():
    weight = float(request.form.get('weight', 0))
    height = float(request.form.get('height', 0))
    if height == 0:
        result = "Invalid height"
    else:
        bmi = weight / ((height/100)**2)
        result = f"BMI: {bmi:.2f}"
    return render_template('index.html', tool="bmi", result=result)

# ---------- DISCOUNT ----------
@app.route('/discount', methods=['POST'])
def discount():
    price = float(request.form.get('price', 0))
    disc = float(request.form.get('discount', 0))
    final = price - (price * disc/100)
    return render_template('index.html', tool="discount", result=f"Final Price: ₹{final:.2f}")

# ---------- WORD COUNT ----------
@app.route('/wordcount', methods=['POST'])
def wordcount():
    text = request.form.get('text', "")
    words = len(text.split())
    return render_template('index.html', tool="wordcount", result=f"Words: {words}")

# ---------- IMAGE RESIZER ----------
@app.route('/resizer', methods=['POST'])
def resizer():
    img = Image.open(request.files['image'])
    w = int(request.form.get('width', 100))
    h = int(request.form.get('height', 100))
    img = img.resize((w, h))
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, download_name="resized.png", as_attachment=True)

# ---------- IMAGE COMPRESS ----------
@app.route('/imgcompress', methods=['POST'])
def imgcompress():
    img = Image.open(request.files['image'])
    quality = int(request.form.get('quality', 70))
    buf = io.BytesIO()
    img.save(buf, format='JPEG', quality=quality)
    buf.seek(0)
    return send_file(buf, download_name="compressed.jpg", as_attachment=True)

# ---------- IMAGE TO PDF ----------
@app.route('/imgtopdf', methods=['POST'])
def imgtopdf():
    img = Image.open(request.files['image'])
    img = img.convert('RGB')

    pdf = FPDF()
    pdf.add_page()

    temp_path = "temp.jpg"
    img.save(temp_path)

    pdf.image(temp_path, x=10, y=10, w=190)

    buf = io.BytesIO()
    pdf.output(buf)
    buf.seek(0)

    return send_file(buf, download_name="image.pdf", as_attachment=True)

# ---------- PDF TO TEXT ----------
@app.route('/pdftotext', methods=['POST'])
def pdftotext():
    file = request.files['pdf']
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return render_template('index.html', tool="pdftotext", result=text)

# ---------- NOTES FORMATTER ----------
@app.route('/notes', methods=['POST'])
def notes():
    content = request.form.get('content', "")
    lines = content.splitlines()
    formatted = "\n".join([f"{i+1}. {line}" for i, line in enumerate(lines)])
    return render_template('index.html', tool="notes", result=formatted)

# ---------- AI BIO ----------
@app.route('/aibio', methods=['POST'])
def aibio():
    name = request.form.get('name', "")
    prof = request.form.get('profession', "")
    hobby = request.form.get('hobbies', "")
    bio = f"{name} is a passionate {prof} who loves {hobby}."
    return render_template('index.html', tool="aibio", result=bio)

# ---------- RESUME ----------
@app.route('/resume', methods=['POST'])
def resume():
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, request.form.get('name', ""), ln=True)

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, request.form.get('email', ""), ln=True)
    pdf.cell(0, 10, request.form.get('phone', ""), ln=True)

    pdf.ln(5)
    pdf.multi_cell(0, 8, "Education:\n" + request.form.get('education', ""))
    pdf.multi_cell(0, 8, "Experience:\n" + request.form.get('experience', ""))
    pdf.multi_cell(0, 8, "Skills:\n" + request.form.get('skills', ""))

    buf = io.BytesIO()
    pdf.output(buf)
    buf.seek(0)

    return send_file(buf, download_name="resume.pdf", as_attachment=True)

# ---------- RUN ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True)
