from flask import Flask, jsonify, request
from udp_client import get_response
from flask_cors import CORS

_, _, students_info = get_response()

app = Flask(__name__)
CORS(app)

# --- 1. GET /api/studentlist ---
@app.route("/api/studentlist", methods=["GET"])
def get_student_list():
    # Return the whole student list as JSON
    # jsonify() converts Python dicts/lists to JSON automatically
    return jsonify(students_info)
# http://127.0.0.1:5000/api/studentlist

# --- 2. GET /api/studentmark/<student-name> ---
@app.route("/api/studentmark/<student_name>", methods=["GET"])
def get_student_mark(student_name):
    # Find the student's mark
    if student_name in students_info:
        return jsonify({student_name: students_info[student_name]})
    else:
        # If not found, return an error message and 404 status code
        return jsonify({"error": "Student not found"}), 404
# http://127.0.0.1:5000/api/studentmark/George
    
# --- 3. POST /api/student ---
@app.route("/api/student", methods=["POST"])
def add_student():
    # Parse JSON payload sent by client (browser or program)
    data = request.get_json()   

    '''
    name = data["student"]
    mark = data["mark"]
    # Add to our "database"
    students_info[name] = mark
    '''

    # data["students"] should be a list of {"student": <name>, "mark": <mark>}
    added_students = []
    for student_entry in data["students"]:
        if "student" in student_entry and "mark" in student_entry:
            name = student_entry["student"]
            mark = student_entry["mark"]
            students_info[name] = mark
            added_students.append(name)
        else:
            return jsonify({"error": "Each entry must contain 'student' and 'mark'"}), 400

    # Return updated student list or confirmation
    return jsonify({"message": f"Added students: {', '.join(added_students)}"}), 201
# Run post.py in another terminal

# --- 4. GET /api/average ---
@app.route("/api/average", methods=["GET"])
def get_class_average():
    if not students_info:
        return jsonify({"average": None, "message": "No students available"}), 200
    
    # Compute the average
    total_marks = sum(students_info.values())
    num_students = len(students_info)
    average = total_marks / num_students
    
    return jsonify({"average": average})
# http://127.0.0.1:5000/api/average

if __name__ == "__main__":
    app.run(debug=True)

# Running on http://127.0.0.1:5000 → This is your server URL.
# Debug mode: on -> Flask will automatically reload if you change your code





