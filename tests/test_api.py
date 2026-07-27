from fastapi.testclient import TestClient
from app.database import Base, engine
from app.main import app

client = TestClient(app)

def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def sample_workflow(workflow_id="loan-1001"):
    return {
        "id": workflow_id,
        "name": "Mortgage Application",
        "events": [
            {"id":"evt-001","timestamp":"2026-07-27T10:00:00Z","type":"APPLICATION_STARTED","status":"success","actor":"customer-101","description":"Application started","metadata":{}},
            {"id":"evt-002","timestamp":"2026-07-27T10:05:00Z","type":"VALIDATION_FAILED","status":"failed","actor":"validation-service","description":"Missing signature","metadata":{}}
        ]
    }

def test_health_check():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {'status':'healthy'}

def test_create_and_read_workflow():
    assert client.post('/api/workflows', json=sample_workflow()).status_code == 201
    response = client.get('/api/workflows/loan-1001')
    assert response.status_code == 200
    assert response.json()['name'] == 'Mortgage Application'

def test_workflow_analytics():
    client.post('/api/workflows', json=sample_workflow())
    response = client.get('/api/workflows/loan-1001/analytics')
    assert response.status_code == 200
    assert response.json()['duration_seconds'] == 300.0
