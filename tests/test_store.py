import allure
import pytest
import requests
import jsonschema
from .schemas.store_schema import STORE_SCHEMA
from .schemas.store_schema import INVENTORY_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Store")
class TestStore:
    @allure.title("Размещение заказа")
    def test_post_placing_order(self):
        with allure.step("Подготовка данных для размещения заказа"):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "shipDate": "2025-11-04T10:05:49.431Z",
                "status": "placed",
                "complete": True
            }

        with allure.step("Отправка запроса на размещения заказа"):
            response = requests.post(url=f"{BASE_URL}/store/order", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200
            jsonschema.validate(response.json(), STORE_SCHEMA)

    @allure.title("Получение информации о заказе по ID")
    def test_get_order_by_id(self, create_order):
        with allure.step("Получение ID созданного заказа"):
            order_id = create_order["id"]

        with allure.step("Отправка запроса на получение информации о заказе по ID"):
            response = requests.get(f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статуса ответа и данных заказа"):
            assert response.status_code == 200
            assert response.json()["id"] == order_id

    @allure.title("Удаление заказа по ID")
    def test_delete_order_by_id(self, create_order):
        with allure.step("Получение ID созданного заказа"):
            order_id = create_order["id"]

        with allure.step("Отправка запроса на удаление заказа"):
            delete_response = requests.delete(f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка успешного удаления"):
            assert delete_response.status_code == 200

        with allure.step("Отправка запроса на получение информации о заказе по ID"):
            response = requests.get(f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статуса ответа и данных заказа"):
            assert response.status_code == 404

        with allure.step("Проверка что заказ действительно удален"):
            get_response_after_delete = requests.get(f"{BASE_URL}/store/order/{order_id}")
            assert get_response_after_delete.status_code == 404

    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_get_information_nonexistent_order(self):
        with allure.step("Отправка запроса на получение информации о несуществующем заказе"):
            response = requests.get(url=f"{BASE_URL}/store/order/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстого содержимого ответа"):
            assert response.text == "Order not found", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Получение инвентаря магазина")
    def test_get_store_inventory(self):
        with allure.step("Отправка запроса на получение инвентаря магазина"):
            response = requests.get(url=f"{BASE_URL}/store/inventory")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response.json(), INVENTORY_SCHEMA)