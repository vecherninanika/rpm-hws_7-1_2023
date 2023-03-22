from requests import get


OK = 200
CREATED = 201
URL = 'http://127.0.0.1:8001/students'
headers = {
    'Authorization': 'admin {a1b2c3d4-a1b2-c3d4-e5f6-a1b2c3a1b2c3}'
}
data = {
    "fname": "a1b2c3d4",
    "lname": "abcdef",
    "group_": "1"
}


def test_requests():
    assert get(URL, headers=headers).status_code == OK
    # assert post(URL, headers=headers, data=data).status_code == CREATED
    # assert get(URL, params=data).status_code == OK
    # assert delete(URL, params=data).status_code == OK


if __name__ == '__main__':
    # here you should use setup_env and setup_db if it was not used before
    test_requests()
