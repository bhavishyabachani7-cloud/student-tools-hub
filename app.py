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
def bmi(): return render_template('index.html', tool="bmi", result=None)

@app.route('/discount', methods=['POST'])
def discount(): return render_template('index.html', tool="discount", result=None)

@app.route('/wordcount', methods=['POST'])
def wordcount(): return render_template('index.html', tool="wordcount", result=None)

@app.route('/cgpa', methods=['POST'])
def cgpa(): return render_template('index.html', tool="cgpa", result=None)

# ---------- AI CAPTION & HOOK GENERATOR ----------
@app.route('/captiongen', methods=['POST'])
def captiongen():
    topic = request.form.get('topic', 'Student productivity').strip()
    tone = request.form.get('tone', 'professional')
    
    if tone == 'trendy':
        result = f"🎯 CURRENT VIBE: ON POINT ⚡\n\nCrushing {topic} right now. No smooth shortcuts, just pure structural execution. Consistency and transparent effort always yield a clean render. ✨\n\n#GrowthTrack #Aesthetic #Build #Focus #Trending"
    elif tone == 'academic':
        result = f"📝 STRUCTURAL RESEARCH ANALYSIS PROFILE\n\nSubject Concept: Critical analysis regarding '{topic}'. Evaluating distinct systematic parameters to optimize core aggregate deliverables. Metrics verified successfully.\n\n#AcademicFramework #ResearchData #Analytics"
    else:
        result = f"💼 EXECUTIVE INSIGHT PROFILE\n\nExcited to share tactical insights regarding {topic}. Emphasizing structured optimization frameworks and strategic development paths to achieve exceptional real-world outcomes.\n\n#ProfessionalGrowth #Leadership #Strategy #Network"
        
    return render_template('index.html', tool="captiongen", result=result)

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

# ---------- PREMIUM MULTI-TEMPLATE RESUME ENGINE ----------
@app.route('/resume', methods=['POST'])
def resume():
    try:
        template = request.form.get('template_id', 'minimal')
        name = request.form.get('name', 'Candidate Profile').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        education = request.form.get('education', '')
        experience = request.form.get('experience', '')
        skills = request.form.get('skills', '')

        pdf = FPDF()
        pdf.add_page()
        
        if template == "modern":
            # DESIGN: NEON MODERN SPLIT ACCENT ARCHITECTURE
            pdf.set_fill_color(0, 255, 200) 
            pdf.rect(0, 0, 8, 297, "F")
            pdf.set_left_margin(18)
            
            pdf.set_text_color(20, 30, 50)
            pdf.set_font("Helvetica", "B", 22)
            pdf.cell(0, 12, name.upper(), ln=True)
            pdf.set_font("Helvetica", "I", 10)
            pdf.cell(0, 6, f"Email Reference: {email} | Contact Link: {phone}", ln=True)
            pdf.ln(10)
            
            def render_modern_section(title, body_data):
                if not body_data.strip(): return
                pdf.set_font("Helvetica", "B", 13)
                pdf.set_text_color(37, 99, 235) 
                pdf.cell(0, 8, title, ln=True)
                pdf.ln(2)
                pdf.set_font("Helvetica", "", 10)
                pdf.set_text_color(60, 60, 70)
                pdf.multi_cell(0, 6, body_data)
                pdf.ln(6)
                
            render_modern_section("Academic Credentials & History", education)
            render_modern_section("Professional Portfolio Track", experience)
            render_modern_section("Core Knowledge Domain Mapping", skills)

        elif template == "executive":
            # DESIGN: EXECUTIVE MANAGEMENT (BOLD HEADER BOX MATRIX)
            pdf.set_fill_color(30, 27, 75) 
            pdf.rect(0, 0, 210, 38, "F")
            
            pdf.set_y(8)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("Helvetica", "B", 20)
            pdf.cell(0, 10, name, ln=True, align="C")
            pdf.set_font("Helvetica", "", 10)
            pdf.cell(0, 6, f"Email: {email}  •  Phone: {phone}", ln=True, align="C")
            
            pdf.set_y(45)
            pdf.set_text_color(40, 40, 50)
            
            def render_exec_section(title, body_data):
                if not body_data.strip(): return
                pdf.set_fill_color(240, 240, 250)
                pdf.set_font("Helvetica", "B", 11)
                pdf.cell(0, 7, f"  {title.upper()}", ln=True, fill=True)
                pdf.ln(2)
                pdf.set_font("Helvetica", "", 10)
                pdf.multi_cell(0, 6, body_data)
                pdf.ln(5)

            render_exec_section("Education Profile", education)
            render_exec_section("Experience Track Record", experience)
            render_exec_section("Core Framework Competencies", skills)

        else:
            # DESIGN: DEFAULT MINIMAL CORPORATE SLATE
            pdf.set_text_color(15, 23, 42)
            pdf.set_font("Helvetica", "B", 20)
            pdf.cell(0, 12, name.upper(), ln=True)
            pdf.set_font("Helvetica", "", 10)
            pdf.cell(0, 6, f"{email}   |   {phone}", ln=True)
            pdf.ln(5)
            
            def render_minimal(title, content):
                if not content.strip(): return
                pdf.set_font("Helvetica", "B", 12)
                pdf.cell(0, 8, title, ln=True)
                pdf.set_draw_color(200, 200, 200)
                pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x()+190, pdf.get_y())
                pdf.ln(3)
                pdf.set_font("Helvetica", "", 10)
                pdf.multi_cell(0, 6, content)
                pdf.ln(5)

            render_minimal("Education Summary", education)
            render_minimal("Professional History", experience)
            render_minimal("Expertise & Skills", skills)

        buf = io.BytesIO()
        pdf.output(buf)
        buf.seek(0)
        return send_file(buf, download_name="premium_resume.pdf", as_attachment=True)
    except Exception as e:
        return f"Document Generator System Error: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
