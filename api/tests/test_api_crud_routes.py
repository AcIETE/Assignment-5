from fastapi import Response
from fastapi.testclient import TestClient
import pytest

from .. import main
from ..dependencies.database import get_db


client = TestClient(main.app)


@pytest.fixture(autouse=True)
def override_db_dependency():
    main.app.dependency_overrides[get_db] = lambda: object()
    yield
    main.app.dependency_overrides.clear()


def test_orders_crud_routes(monkeypatch):
    monkeypatch.setattr(main.orders, "create", lambda db, order: {"id": 1, "customer_name": order.customer_name, "description": order.description, "order_date": None, "order_details": []})
    monkeypatch.setattr(main.orders, "read_all", lambda db: [{"id": 1, "customer_name": "Alice", "description": "first", "order_date": None, "order_details": []}])
    monkeypatch.setattr(main.orders, "read_one", lambda db, order_id: None if order_id == 999 else {"id": order_id, "customer_name": "Alice", "description": "first", "order_date": None, "order_details": []})
    monkeypatch.setattr(main.orders, "update", lambda db, order_id, order: {"id": order_id, "customer_name": "Alice", "description": order.description or "first", "order_date": None, "order_details": []})
    monkeypatch.setattr(main.orders, "delete", lambda db, order_id: Response(status_code=204))

    response = client.post("/orders/", json={"customer_name": "Alice", "description": "first"})
    assert response.status_code == 200

    response = client.get("/orders/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    response = client.get("/orders/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

    response = client.put("/orders/1", json={"description": "updated"})
    assert response.status_code == 200
    assert response.json()["description"] == "updated"

    response = client.delete("/orders/1")
    assert response.status_code == 204

    response = client.get("/orders/999")
    assert response.status_code == 404


def test_sandwiches_crud_routes(monkeypatch):
    monkeypatch.setattr(main.sandwiches, "create", lambda db, sandwich: {"id": 1, "sandwich_name": sandwich.sandwich_name, "price": sandwich.price})
    monkeypatch.setattr(main.sandwiches, "read_all", lambda db: [{"id": 1, "sandwich_name": "Club", "price": 8.5}])
    monkeypatch.setattr(main.sandwiches, "read_one", lambda db, sandwich_id: None if sandwich_id == 999 else {"id": sandwich_id, "sandwich_name": "Club", "price": 8.5})
    monkeypatch.setattr(main.sandwiches, "update", lambda db, sandwich_id, sandwich: {"id": sandwich_id, "sandwich_name": sandwich.sandwich_name or "Club", "price": sandwich.price or 8.5})
    monkeypatch.setattr(main.sandwiches, "delete", lambda db, sandwich_id: Response(status_code=204))

    response = client.post("/sandwiches/", json={"sandwich_name": "Club", "price": 8.5})
    assert response.status_code == 200

    response = client.get("/sandwiches/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    response = client.get("/sandwiches/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

    response = client.put("/sandwiches/1", json={"price": 9.25})
    assert response.status_code == 200
    assert response.json()["price"] == 9.25

    response = client.delete("/sandwiches/1")
    assert response.status_code == 204

    response = client.get("/sandwiches/999")
    assert response.status_code == 404


def test_resources_crud_routes(monkeypatch):
    monkeypatch.setattr(main.resources, "create", lambda db, resource: {"id": 1, "item": resource.item, "amount": resource.amount})
    monkeypatch.setattr(main.resources, "read_all", lambda db: [{"id": 1, "item": "Bread", "amount": 50}])
    monkeypatch.setattr(main.resources, "read_one", lambda db, resource_id: None if resource_id == 999 else {"id": resource_id, "item": "Bread", "amount": 50})
    monkeypatch.setattr(main.resources, "update", lambda db, resource_id, resource: {"id": resource_id, "item": resource.item or "Bread", "amount": resource.amount or 50})
    monkeypatch.setattr(main.resources, "delete", lambda db, resource_id: Response(status_code=204))

    response = client.post("/resources/", json={"item": "Bread", "amount": 50})
    assert response.status_code == 200

    response = client.get("/resources/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    response = client.get("/resources/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

    response = client.put("/resources/1", json={"amount": 40})
    assert response.status_code == 200
    assert response.json()["amount"] == 40

    response = client.delete("/resources/1")
    assert response.status_code == 204

    response = client.get("/resources/999")
    assert response.status_code == 404


def test_recipes_crud_routes(monkeypatch):
    monkeypatch.setattr(main.recipes, "create", lambda db, recipe: {"id": 1, "amount": recipe.amount, "sandwich": {"id": 1, "sandwich_name": "Club", "price": 8.5}, "resource": {"id": 1, "item": "Bread", "amount": 50}})
    monkeypatch.setattr(main.recipes, "read_all", lambda db: [{"id": 1, "amount": 2, "sandwich": {"id": 1, "sandwich_name": "Club", "price": 8.5}, "resource": {"id": 1, "item": "Bread", "amount": 50}}])
    monkeypatch.setattr(main.recipes, "read_one", lambda db, recipe_id: None if recipe_id == 999 else {"id": recipe_id, "amount": 2, "sandwich": {"id": 1, "sandwich_name": "Club", "price": 8.5}, "resource": {"id": 1, "item": "Bread", "amount": 50}})
    monkeypatch.setattr(main.recipes, "update", lambda db, recipe_id, recipe: {"id": recipe_id, "amount": recipe.amount or 2, "sandwich": {"id": 1, "sandwich_name": "Club", "price": 8.5}, "resource": {"id": 1, "item": "Bread", "amount": 50}})
    monkeypatch.setattr(main.recipes, "delete", lambda db, recipe_id: Response(status_code=204))

    response = client.post("/recipes/", json={"sandwich_id": 1, "resource_id": 1, "amount": 2})
    assert response.status_code == 200

    response = client.get("/recipes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    response = client.get("/recipes/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

    response = client.put("/recipes/1", json={"amount": 3})
    assert response.status_code == 200
    assert response.json()["amount"] == 3

    response = client.delete("/recipes/1")
    assert response.status_code == 204

    response = client.get("/recipes/999")
    assert response.status_code == 404


def test_order_details_crud_routes(monkeypatch):
    monkeypatch.setattr(main.order_details, "create", lambda db, order_detail: {"id": 1, "amount": order_detail.amount, "order_id": order_detail.order_id, "sandwich": {"id": 1, "sandwich_name": "Club", "price": 8.5}})
    monkeypatch.setattr(main.order_details, "read_all", lambda db: [{"id": 1, "amount": 1, "order_id": 1, "sandwich": {"id": 1, "sandwich_name": "Club", "price": 8.5}}])
    monkeypatch.setattr(main.order_details, "read_one", lambda db, order_detail_id: None if order_detail_id == 999 else {"id": order_detail_id, "amount": 1, "order_id": 1, "sandwich": {"id": 1, "sandwich_name": "Club", "price": 8.5}})
    monkeypatch.setattr(main.order_details, "update", lambda db, order_detail_id, order_detail: {"id": order_detail_id, "amount": order_detail.amount or 1, "order_id": order_detail.order_id or 1, "sandwich": {"id": 1, "sandwich_name": "Club", "price": 8.5}})
    monkeypatch.setattr(main.order_details, "delete", lambda db, order_detail_id: Response(status_code=204))

    response = client.post("/order_details/", json={"order_id": 1, "sandwich_id": 1, "amount": 1})
    assert response.status_code == 200

    response = client.get("/order_details/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    response = client.get("/order_details/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

    response = client.put("/order_details/1", json={"amount": 2})
    assert response.status_code == 200
    assert response.json()["amount"] == 2

    response = client.delete("/order_details/1")
    assert response.status_code == 204

    response = client.get("/order_details/999")
    assert response.status_code == 404
