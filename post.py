import requests

url = "http://127.0.0.1:5000/api/student"

students_to_add = [
    {"student": "Alice", "mark": 92},
    {"student": "Bob", "mark": 85},
    {"student": "Hugo", "mark": 100},
]

payload = {"students": students_to_add}
r = requests.post(url, json=payload)

if r.status_code == 201:
    print("Successfully added students!")
    print(r.json())
else:
    print("Error:", r.json())