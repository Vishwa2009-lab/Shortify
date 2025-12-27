import os

# Create folder structure
os.makedirs('shortify-ai/templates', exist_ok=True)
os.makedirs('shortify-ai/static', exist_ok=True)
os.makedirs('shortify-ai/uploads', exist_ok=True)

# Create requirements.txt
with open('shortify-ai/requirements.txt', 'w') as f:
    f.write('flask\nmoviepy')

# Create app.py
app_py = '''from flask import Flask, render_template, request, send_file
import os
from moviepy.editor import VideoFileClip

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process_video():
    file = request.files["video"]
    duration = int(request.form["duration"])

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    clip = VideoFileClip(path)

    short = clip.subclip(0, min(duration, clip.duration))

    w, h = short.size
    target_ratio = 9/16
    new_width = int(h * target_ratio)
    x1 = (w - new_width) // 2
    x2 = x1 + new_width
    short = short.crop(x1=x1, x2=x2)

    output_path = os.path.join(UPLOAD_FOLDER, "short_" + file.filename)
    short.write_videofile(output_path)

    clip.close()
    short.close()

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)'''

with open('shortify-ai/app.py', 'w') as f:
    f.write(app_py)

# Create index.html
templates_html = '''<!DOCTYPE html>
<html>
<head>
  <title>Shortify AI</title>
  <link rel="stylesheet" href="/static/style.css">
</head>
<body>

<h1>Shortify AI</h1>
<p>Make Shorts Instantly</p>

<form action="/process" method="POST" enctype="multipart/form-data">
  <label>Upload video (copyright-free or your own)</label><br>
  <input type="file" name="video" required><br><br>

  <label>Choose duration</label><br>
  <select name="duration">
    <option value="15">15 seconds</option>
    <option value="30">30 seconds</option>
    <option value="45">45 seconds</option>
    <option value="60">60 seconds</option>
  </select><br><br>

  <button type="submit">Generate Short</button>
</form>

</body>
</html>'''

with open('shortify-ai/templates/index.html', 'w') as f:
    f.write(templates_html)

# Create style.css
style_css = '''body{
  font-family: Arial;
  background:#0f0f0f;
  color:white;
  text-align:center;
  padding-top:40px;
}
h1{
  font-size:40px;
}
form{
  margin-top:30px;
  background:#181818;
  display:inline-block;
  padding:25px 35px;
  border-radius:20px;
}
button{
  padding:10px 20px;
  border-radius:12px;
  border:none;
  font-size:16px;
  cursor:pointer;
}'''

with open('shortify-ai/static/style.css', 'w') as f:
    f.write(style_css)

print('Shortify AI folder created successfully! Download it from your system.')