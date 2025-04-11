from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Set up database
def setup_database():
    conn = sqlite3.connect("specimen_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS specimens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            microscope_size REAL,
            magnification REAL,
            actual_size REAL
        )
    """)
    conn.commit()
    conn.close()

# Save data to database
def save_to_database(username, microscope_size, magnification, actual_size):
    conn = sqlite3.connect("specimen_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO specimens (username, microscope_size, magnification, actual_size)
        VALUES (?, ?, ?, ?)
    """, (username, microscope_size, magnification, actual_size))
    conn.commit()
    conn.close()

# Home route
@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        try:
            username = request.form["username"]
            microscope_size = float(request.form["microscope_size"])
            magnification = float(request.form["magnification"])

            if magnification == 0:
                result = "Magnification cannot be zero."
            else:
                actual_size = microscope_size / magnification
                save_to_database(username, microscope_size, magnification, actual_size)
                result = f"Real-life size: {actual_size:.4f} μm"
        except:
            result = "Please enter valid numbers."

    return render_template("index.html", result=result)

if __name__ == "__main__":
    setup_database()
    app.run(debug=True)
