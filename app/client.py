import requests

def main():
    # User input
    username = input("Enter username: ")
    password = input("Enter password: ")

    # Send request to /api/submit
    submit_url = "http://127.0.0.1:5000/api/submit"
    submit_data = {'username': username, 'password': password}
    submit_response = requests.post(submit_url, json=submit_data)
    encoded_password = submit_response.json().get('encoded_password')

    print(f"Password Submitted! ")

    # Send request to /api/retrieve
    retrieve_url = "http://127.0.0.1:5000/api/retrieve"
    retrieve_data = {'username': username}
    retrieve_response = requests.post(retrieve_url, json=retrieve_data)
    retrieved_data = retrieve_response.json()

    print(f"Retrieved Data: Encoded Password: {retrieved_data['encoded_password']}, Decoded Password: {retrieved_data['decoded_password']}")

if __name__ == '__main__':
    main()
