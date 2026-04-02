import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange: Nenhum setup necessário, pois os dados são in-memory
    
    # Act: Fazer requisição GET para /activities
    resp = client.get("/activities")
    
    # Assert: Verificar status e conteúdo
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data

def test_signup_for_activity():
    # Arrange: Definir atividade e email para teste
    activity_name = "Chess Club"
    email = "test-user@mergington.edu"
    
    # Act: Fazer requisição POST para signup
    resp = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert: Verificar sucesso e mensagem
    assert resp.status_code == 200
    assert "Signed up test-user@mergington.edu for Chess Club" in resp.json()["message"]

def test_signup_duplicate_fails():
    # Arrange: Inscrever um email primeiro
    email = "duplicate@mergington.edu"
    client.post("/activities/Programming Class/signup", params={"email": email})
    
    # Act: Tentar inscrever o mesmo email novamente
    resp = client.post("/activities/Programming Class/signup", params={"email": email})
    
    # Assert: Verificar erro de duplicata
    assert resp.status_code == 400
    assert "already signed up" in resp.json()["detail"].lower()

def test_signup_activity_not_found():
    # Arrange: Usar atividade inexistente
    activity_name = "Nonexistent"
    email = "x@x.com"
    
    # Act: Tentar signup
    resp = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    
    # Assert: Verificar erro 404
    assert resp.status_code == 404
    assert "Activity not found" in resp.json()["detail"]

def test_remove_participant_success():
    # Arrange: Usar participante existente
    activity_name = "Chess Club"
    email = "daniel@mergington.edu"  # Já inscrito
    
    # Act: Remover o participante
    resp = client.delete(f"/activities/{activity_name}/participants", params={"email": email})
    
    # Assert: Verificar sucesso
    assert resp.status_code == 200
    assert "Removed daniel@mergington.edu from Chess Club" in resp.json()["message"]

def test_remove_participant_not_found():
    # Arrange: Email que não está inscrito
    activity_name = "Chess Club"
    email = "nobody@x.com"
    
    # Act: Tentar remover
    resp = client.delete(f"/activities/{activity_name}/participants", params={"email": email})
    
    # Assert: Verificar erro 404
    assert resp.status_code == 404
    assert "Participant not found" in resp.json()["detail"]

def test_remove_from_nonexistent_activity():
    # Arrange: Atividade inexistente
    activity_name = "NoClub"
    email = "a@b.com"
    
    # Act: Tentar remover
    resp = client.delete(f"/activities/{activity_name}/participants", params={"email": email})
    
    # Assert: Verificar erro 404
    assert resp.status_code == 404
    assert "Activity not found" in resp.json()["detail"]