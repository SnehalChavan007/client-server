import socket
import xml.etree.ElementTree as ET
import mysql.connector

def save_xml_file(data):
    with open("data.xml", "wb") as f:
        f.write(data)
    print("Data saved to XML file.")

def parse_data(data):
    root = ET.fromstring(data)
    name = root.find('Name').text
    email = root.find('Email').text
    ID = root.find('ID').text
    return name, email, ID

def store_data(name, email, ID):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Root@123",
            database="employee_data"
        )

        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS employee
                      (name VARCHAR(255), email VARCHAR(255), ID INT)''')
        
        cursor.execute("SELECT * FROM employee WHERE name = %s AND email = %s AND ID = %s", (name, email, ID))
        result = cursor.fetchone()
        
        if result:
            print("Data already exists in the database. Skipping insertion.")
        else:
            cursor.execute("INSERT INTO employee (name, email, ID) VALUES (%s, %s, %s)", (name, email, ID))
            connection.commit()
            print("Data inserted successfully.")

    except mysql.connector.Error as error:
        if connection:
            connection.rollback()
        print("Error inserting data:", error)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def main():
    try:
        server_socket = socket.socket()
        print("Server Created")
        server_socket.bind(('172.17.0.1', 9992))
        server_socket.listen(2)
        print("Waiting for Connection")
        client_socket, address = server_socket.accept()
        print(f"Connection from {address} established.")
        
        data = client_socket.recv(1024)
        print("Received data from client: ")
        print(data.decode())
        save_xml_file(data)
        client_socket.close()
        
        name, email, ID = parse_data(data)
        store_data(name, email, ID)
        print("Data received and stored successfully.")
    
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
