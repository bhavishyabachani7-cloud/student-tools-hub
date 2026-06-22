from flask import Flask, render_template, request, send_file, Response
from fpdf import FPDF
import io
import PyPDF2

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/', methods=['GET', 'HEAD'])
def home():
    if request.method == 'HEAD':
        return Response(status=200)
    return render_template('index.html', tool="bmi", result=None)

# JavaScript handles calculations instantly, but endpoints catch fallback requests safely
@app.route('/bmi', methods=['POST'])
def bmi():
    return render_template('index.html', tool="bmi", result=None)

@app.route('/discount', methods=['POST'])
def discount():
    return render_template('index.html', tool="discount", result=None)

@app.route('/wordcount', methods=['POST'])
def wordcount():
    return render_template('index.html', tool="wordcount", result=None)

@app.route('/cgpa', methods=['POST'])
def cgpa():
    return render_template('index.html', tool="cgpa", result=None)

# ---------- PDF TO TEXT ENGINE ----------
@app.route('/pdftotext', methods=['POST'])
def pdftotext():
    file = request.files.get('pdf')
    if not file or file.filename == '':
        return render_template('index.html', tool="pdftotext", result="Error: No file uploaded.")
    try:
        reader = PyPDF2.PdfReader(file)
        text = "".join([p.extract_text() or "" for p in reader.pages])
        if not text.strip():
            text = "Extraction complete: No readable text layers detected in this document."
    except Exception as e:
        text = f"Processing Error: Could not compile data stream ({str(e)})"
    return render_template('index.html', tool="pdftotext", result=text)

# ---------- NOTES FORMATTER ----------
@app.route('/notes', methods=['POST'])
def notes():
    content = request.form.get('content', "")
    lines = content.splitlines()
    formatted = "\n".join([f"{i+1}. {l.strip()}" for i, l in enumerate(lines) if l.strip()])
    return render_template('index.html', tool="notes", result=formatted if formatted else "No content to format.")

# ---------- AI BIO GENERATOR ----------
@app.route('/aibio', methods=['POST'])
def aibio():
    name = request.form.get('name', "The Individual").strip()
    profession = request.form.get('profession', "Innovator").strip()
    hobbies = request.form.get('hobbies', "exploring specialized concepts").strip()
    
    result = f"⚡ {name} is a dedicated professional specializing in {profession}. Driven by structural curiosity, they focus their personal time on {hobbies}, bridging theoretical knowledge with practical execution frameworks."
    return render_template('index.html', tool="aibio", result=result)

# ---------- MODERN RESUME BUILDER ----------
@app.route('/resume', methods=['POST'])
def resume():
    try:
        pdf = FPDF()
        pdf.add_page()
        
        # Primary Identity Title Bar
        pdf.set_text_color(15, 23, 42)
        pdf.set_font("Helvetica", "B", 20)
        pdf.cell(0, 12, request.form.get('name', 'Candidate Name').upper(), ln=True, align='L')
        
        # Sub-heading Metadata links
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(100, 116, 139)
        contact = f"Email: {request.form.get('email', '')}   |   Phone: {request.form.get('phone', '')}"
        pdf.cell(0, 6, contact, ln=True, align='L')
        pdf.ln(8)
        
        # Section Generator Component
        def render_section(title, data):
            if not data.strip(): return
            pdf.set_font("Helvetica", "B", 12)
            pdf.set_text_color(138, 43, 226) # Royal Blue Accent Theme
            pdf.cell(0, 8, title.upper(), ln=True)
            
            # Decorative break horizontal rule lines
            pdf.set_draw_color(226, 232, 240)
            pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 190, pdf.get_y())
            pdf.ln(4)
            
            # Content Context Strings
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(51, 65, 85)
            pdf.multi_cell(0, 6, data)
            pdf.ln(6)

        render_section("Education & Credentials", request.form.get('education', ''))
        render_section("Professional Experience Track", request.form.get('experience', ''))
        render_section("Core Knowledge Domain Skills", request.form.get('skills', ''))

        buf = io.BytesIO()
        pdf.output(buf)
        buf.seek(0)
        return send_file(buf, download_name="executive_resume.pdf", as_attachment=True)
    except Exception as e:
        return f"Document Generator System Error: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
