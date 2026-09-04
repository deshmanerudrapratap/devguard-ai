def test_health_ok(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["service"] == "DevGuard AI"
    assert body["database"] == "connected"


def test_dashboard_summary_has_no_fake_analysis(client):
    response = client.get("/api/dashboard/summary")
    assert response.status_code == 200
    body = response.json()
    assert body["repository_count"] == 0
    assert body["analysis_runs"] == 0
    assert all(agent["status"] == "not_implemented" for agent in body["agents"])


def test_register_and_list_repository(client):
    create = client.post(
        "/api/repositories",
        json={
            "name": "demo-target",
            "local_path": "D:/devguard-ai/demo-target",
            "description": "Sample workspace",
        },
    )
    assert create.status_code == 201
    payload = create.json()
    assert payload["name"] == "demo-target"
    assert payload["id"] >= 1

    listed = client.get("/api/repositories")
    assert listed.status_code == 200
    assert len(listed.json()) == 1


def test_register_requires_location(client):
    response = client.post("/api/repositories", json={"name": "empty"})
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"


def test_duplicate_name_conflict(client):
    body = {"name": "same", "remote_url": "https://example.com/org/repo.git"}
    assert client.post("/api/repositories", json=body).status_code == 201
    conflict = client.post("/api/repositories", json=body)
    assert conflict.status_code == 409
    assert conflict.json()["error"]["code"] == "conflict"


def test_delete_missing_repository(client):
    response = client.delete("/api/repositories/999")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "not_found"
