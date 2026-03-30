from flask import Flask, render_template, request, send_file, Response
from fpdf import FPDF
import io
import PyPDF2

app = Flask(__name__)

# ---------- HOME ----------
@app.route('/', methods=['GET', 'HEAD'])
def home():
    if request.method == 'HEAD':
        return Response(status=200)
    return render_template('index.html', tool="bmi", result=None)

# ---------- BMI ----------
@app.route('/bmi', methods=['POST'])
def bmi():
    try:
        w = float(request.form.get('weight', 0))
        h = float(request.form.get('height', 0))
        result = f"BMI: {w/((h/100)**2):.2f}" if h != 0 else "Invalid height"
    except:
        result = "Error"
    return render_template('index.html', tool="bmi", result=result)

# ---------- DISCOUNT ----------
@app.route('/discount', methods=['POST'])
def discount():
    try:
        p = float(request.form.get('price', 0))
        d = float(request.form.get('discount', 0))
        result = f"Final Price: ₹{p-(p*d/100):.2f}"
    except:
        result = "Error"
    return render_template('index.html', tool="discount", result=result)

# ---------- WORD COUNT ----------
@app.route('/wordcount', methods=['POST'])
def wordcount():
    text = request.form.get('text', "")
    result = f"Words: {len(text.split())}"
    return render_template('index.html', tool="wordcount", result=result)

# ---------- PDF TO TEXT ----------
@app.route('/pdftotext', methods=['POST'])
def pdftotext():
    file = request.files.get('pdf')
    if not file:
        return "No file uploaded"

    reader = PyPDF2.PdfReader(file)
    text = "".join([p.extract_text() or "" for p in reader.pages])

    return render_template('index.html', tool="pdftotext", result=text)

# ---------- NOTES ----------
@app.route('/notes', methods=['POST'])
def notes():
    content = request.form.get('content', "")
    lines = content.splitlines()
    formatted = "\n".join([f"{i+1}. {l}" for i, l in enumerate(lines)])

    return render_template('index.html', tool="notes", result=formatted)

# ---------- AI BIO ----------
@app.route('/aibio', methods=['POST'])
def aibio():
    n = request.form.get('name', "")
    p = request.form.get('profession', "")
    h = request.form.get('hobbies', "")

    result = f"{n} is a passionate {p} who loves {h}."
    return render_template('index.html', tool="aibio", result=result)

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

    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    buf = io.BytesIO(pdf_bytes)

    return send_file(buf, download_name="resume.pdf", as_attachment=True)

# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True)
