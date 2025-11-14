import socket

def get_response():
    # Server details — same port the server is listening on
    SERVER_IP = '149.171.37.163'   # if client runs on same machine as server
    SERVER_PORT = 5000

    # Create a UDP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # The request message expected by server
    request_msg = 'studentmarklist' + '\0'

    # Send the message
    s.sendto(request_msg.encode(), (SERVER_IP, SERVER_PORT))
    print(f"Sent request: {request_msg}")

    # Wait for response
    data, addr = s.recvfrom(1024)
    response = data.decode()
    response_wo_num_students = response[4:]
    print(f"Received response from {addr}:")
    print(response)
    print(response_wo_num_students)

    # Format the response
    num_students_str = response[0:4]
    print("No. Students: " + num_students_str)

    name_len = 16
    mark_len = 4
    record_len = name_len + mark_len
    num_students_bytes = 4      # the number of students is represented in the first 4 bytes

    print(f"{'Name':<16} | {'Mark':>4}")
    print("-" * 23)

    students_info = {}

    num_students_int = int(num_students_str)
    for i in range(num_students_int):
        start_idx = (i * record_len) + num_students_bytes 
        name = response[start_idx:start_idx + name_len].rstrip('\0')
        mark = response[start_idx + name_len:start_idx + record_len].rstrip('\0')

        print(f"{name:<16} | {mark:>4}")

        students_info[name] = int(mark)

    print(students_info)

    # Close socket
    print("Closing")
    s.close()

    return response_wo_num_students, num_students_int, students_info
