import socket
import re

def send_data(name, email, ID):
    xml_data = f"<KPIT>\n<Name>{name}</Name>\n<Email>{email}</Email>\n<ID>{ID}</ID>\n</KPIT>"
    
    client_socket = socket.socket()
    client_socket.connect(('172.17.0.1', 9992))
    client_socket.send(xml_data.encode())
    print("Data sent to server successfully.")
    client_socket.close()

def validate_input(name, email, ID):
    if not name.isalpha():
        print("Name should contain characters.")
        return False
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        print("Invalid email format.")
        return False
    if not ID.isdigit():
        print("ID must be a positive integer.")
        return False
    return True

def main():
    name = input("Enter name: ")
    email = input("Enter email: ")
    ID = input("Enter ID: ")

    if validate_input(name, email, ID):
        send_data(name, email, ID)
    else:
        main()

if __name__ == "__main__":
    main()