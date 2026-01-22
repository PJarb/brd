# data/mock_requirements.py
MOCK_REQUIREMENTS = [
    {
        "id": 1,
        "text": "ระบบต้องรองรับการเข้าสู่ระบบผ่าน Google Account ได้",
        "status": "Clear",
        "category": "Functional",
        "issue": None,
        "suggestion": None,
        "testCase": "Scenario: Login with Google..."
    },
    {
        "id": 2,
        "text": "หน้า Dashboard ควรจะโหลดได้เร็วๆ และใช้งานง่าย",
        "status": "Unclear",
        "category": "Non-Functional",
        "issue": "คำว่าเร็วๆ ไม่ชัดเจน",
        "suggestion": "ระบุ SLA เช่น โหลด < 2 วินาที"
    }
]
