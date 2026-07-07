import urllib.request
import json

BASE_URL = "http://127.0.0.1:8000"

def post_json(path, data, token=None):
    url = BASE_URL + path
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = f"Bearer {token}"

    data_bytes = json.dumps(data).encode('utf-8')

    req = urllib.request.Request(url, data=data_bytes, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8')), response.status
    except urllib.error.HTTPError as e:
        print(f"Error {e.code}: {e.read().decode('utf-8')}")
        return None, e.code

def seed_data():
    print("Starting data seeding...")
    
    # 1. Login to get token
    res, status = post_json("/auth/login", {"username": "admin", "password": "admin123"})
    if status != 200 or not res:
        print("Failed to login")
        return
        
    token = res.get("data", {}).get("access_token")
    print("Logged in successfully.")

    # 2. Add Readers
    readers = [
        {"reader_code": "DG001", "full_name": "Nguyễn Văn A", "email": "nva@example.com", "phone": "0901234567", "address": "Hà Nội"},
        {"reader_code": "DG002", "full_name": "Trần Thị B", "email": "ttb@example.com", "phone": "0912345678", "address": "TP HCM"},
        {"reader_code": "DG003", "full_name": "Lê Văn C", "email": "lvc@example.com", "phone": "0923456789", "address": "Đà Nẵng"}
    ]
    for r in readers:
        post_json("/readers", r, token)
    print("Added readers.")

    # 3. Add Documents
    docs = [
        {
            "title": "Clean Code",
            "author": "Robert C. Martin",
            "publisher": "Prentice Hall",
            "publish_year": 2008,
            "category": "Lập trình",
            "isbn": "9780132350884",
            "description": "Sách hay về cách viết code sạch"
        },
        {
            "title": "Nhà Giả Kim",
            "author": "Paulo Coelho",
            "publisher": "NXB Hội Nhà Văn",
            "publish_year": 1988,
            "category": "Tiểu thuyết",
            "isbn": "9786045332630",
            "description": "Hành trình đi tìm kho báu"
        },
        {
            "title": "Dế Mèn Phiêu Lưu Ký",
            "author": "Tô Hoài",
            "publisher": "NXB Kim Đồng",
            "publish_year": 1941,
            "category": "Thiếu nhi",
            "isbn": "123456789",
            "description": "Câu chuyện kinh điển"
        }
    ]
    for d in docs:
        doc_res, doc_status = post_json("/documents", d, token)
        if doc_status == 200 and doc_res:
            doc_id = doc_res["data"]["id"]
            post_json(f"/documents/{doc_id}/copies", {"quantity": 3}, token)
    print("Added documents with 3 copies each.")

    print("Data seeding completed successfully!")

if __name__ == "__main__":
    seed_data()
