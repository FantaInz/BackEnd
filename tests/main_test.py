from fastapi.testclient import TestClient



from app.main import server



client = TestClient(server)

