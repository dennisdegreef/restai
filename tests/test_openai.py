from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "RESTAI, so many 'A's and 'I's, so little time..."


def test_getProjects():
    response = client.get("/projects")
    assert response.status_code == 200
    assert response.json() == {"projects": []}


def test_createProject():
    response = client.post(
        "/projects", json={"name": "test_openai",  "embeddings": "openai", "llm": "openai"})
    assert response.status_code == 200
    
def test_getProject():
    response = client.get("/projects/test_openai")
    assert response.status_code == 200
    
def test_createProject2():
    response = client.post(
        "/projects", json={"name": "test_openai2",  "embeddings": "openai", "llm": "openai"})
    assert response.status_code == 200
    
def test_getProjects2():
    response = client.get("/projects")
    assert response.status_code == 200
    assert response.json() == {"projects": ['test_openai', 'test_openai2']}


def test_ingestURL():
    response = client.post("/projects/test_openai/embeddings/ingest/url",
                           json={"url": "https://www.google.com"})
    assert response.status_code == 200


def test_getProjectAfterIngestURL():
    response = client.get("/projects/test_openai")
    assert response.status_code == 200
    assert response.json() == {
        "project": "test_openai", "llm": "openai", "embeddings": "openai", "documents": 1, "metadatas": 1}


def test_ingestUpload():
    response = client.post("/projects/test_openai/embeddings/ingest/upload",
                           files={"file": ("test.txt", open("tests/test.txt", "rb"))})
    assert response.status_code == 200

def test_getProjectAfterIngestUpload():
    response = client.get("/projects/test_openai")
    assert response.status_code == 200
    assert response.json() == {
        "project": "test_openai", "llm":"openai", "embeddings": "openai", "documents": 2, "metadatas": 2}
    
def test_ingestUpload2():
    response = client.post("/projects/test_openai/embeddings/ingest/upload",
                           files={"file": ("test2.txt", open("tests/test2.txt", "rb"))})
    assert response.status_code == 200

def test_getEmbeddings():
    response = client.post("/projects/test_openai/embeddings/find", json={"source": "test2.txt"})
    assert response.status_code == 200
    assert len(response.json()["ids"]) == 1

def test_deleteEmbeddings():
    response = client.post("/projects/test_openai/embeddings/delete", json={"source": "test2.txt"})
    assert response.status_code == 200
    assert response.json() == {"deleted": 1}
    
def test_getEmbeddingsAfterDelete():
    response = client.post("/projects/test_openai/embeddings/find", json={"source": "test2.txt"})
    assert response.status_code == 200
    assert len(response.json()["ids"]) == 0

def test_questionProject():
    response = client.post("/projects/test_openai/question",
                           json={"question": "What is the secret?"})
    assert response.status_code == 200
    assert response.json() == {"question": "What is the secret?",
                               "answer": "The secret is that ingenuity should be bigger than politics and corporate greed."}

def test_questionProject2():
    response = client.post("/projects/test_openai2/question",
                           json={"question": "What is the secret?"})
    assert response.status_code == 200
    assert "ingenuity" not in response.json()["answer"]

def test_questionSystemProject():
    response = client.post("/projects/test_openai/question",
                           json={"system": "You are a digital assistant, answer only in french.", "question": "What is the secret?"})
    assert response.status_code == 200
    assert "Le secret" in response.json()["answer"]

def test_chatProject():
    response1 = client.post("/projects/test_openai/chat",
                            json={"message": "What is the secret?"})
    assert response1.status_code == 200
    output1 = response1.json()
    response2 = client.post("/projects/test_openai/chat",
                            json={"message": "Do you agree with this secret?", "id": output1["id"]})
    assert response2.status_code == 200
    output2 = response2.json()

def test_resetProject():
    response = client.post("/projects/test_openai/embeddings/reset")
    assert response.status_code == 200
    
def test_questionProjectAfterReset():
    response = client.post("/projects/test_openai/question",
                           json={"question": "What is the secret?"})
    assert response.status_code == 200
    assert "ingenuity" not in response.json()["answer"]
    
def test_getProjectAfterIngestUploadAfterReset():
    response = client.get("/projects/test_openai")
    assert response.status_code == 200
    assert response.json() == {
        "project": "test_openai", "llm": "openai", "embeddings": "openai", "documents": 0, "metadatas": 0}
    
def test_ingestUploadAfterReset():
    response = client.post("/projects/test_openai/embeddings/ingest/upload",
                           files={"file": ("test.txt", open("tests/test.txt", "rb"))})
    assert response.status_code == 200
    
def test_questionProjectAfterResetAfterIngest():
    response = client.post("/projects/test_openai/question",
                           json={"question": "What is the secret?"})
    assert response.status_code == 200
    assert response.json() == {"question": "What is the secret?",
                               "answer": "The secret is that ingenuity should be bigger than politics and corporate greed."}

def test_deleteProject():
    response = client.delete("/projects/test_openai")
    assert response.status_code == 200
    assert response.json() == {"project": "test_openai"}

def test_deleteProject2():
    response = client.delete("/projects/test_openai2")
    assert response.status_code == 200
    assert response.json() == {"project": "test_openai2"}

def test_getProjectAfterDelete():
    response = client.get("/projects/test_openai")
    assert response.status_code == 404


def test_getProjectsAfterDelete():
    response = client.get("/projects")
    assert response.status_code == 200
    assert response.json() == {"projects": []}
