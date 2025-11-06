import allure
import pytest
import requests

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
                "status": "placed",
                "complete": True
            }

        with allure.step("Отправка запроса на размещения заказа"):
            response = requests.post(url=f"{BASE_URL}/store/order", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json['id'] == payload['id'], "id заказ не совпадает с ожидаемым"
            assert response_json['petId'] == payload['petId'], "petId заказа не совпадает с ожидаемым"
            assert response_json['quantity'] == payload['quantity'], "quantity заказов не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "status заказа не совпадает с ожидаемым"
            assert response_json['complete'] == payload['complete'], "complete не совпадает с ожидаемым"

    @allure.title("Получение информации о заказе по ID")
    def test_get_order_by_id(self):
        with allure.step("Получение ID созданного заказа"):
            order_id = 1

        with allure.step("Отправка запроса на получение информации о заказе по ID"):
            response = requests.get(f"{BASE_URL}/store/order/1")

        with allure.step("Проверка статуса ответа и данных заказа"):
            assert response.status_code == 200
            assert response.json()["id"] == order_id

    @allure.title("Удаление заказа по ID")
    def test_delete_order_by_id(self):
        with allure.step("Получение ID созданного заказа"):
            order_id = 1

        with allure.step("Отправка запроса на удаление заказа"):
            delete_response = requests.delete(f"{BASE_URL}/store/order/1")

        with allure.step("Проверка успешного удаления"):
            assert delete_response.status_code == 200

        with allure.step("Отправка запроса на получение информации о заказе по ID"):
            response = requests.get(f"{BASE_URL}/store/order/1")

        with allure.step("Проверка статуса ответа и данных заказа"):
            assert response.status_code == 404

        with allure.step("Проверка что заказ действительно удален"):
            get_response_after_delete = requests.get(f"{BASE_URL}/store/order/1")
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

        with allure.step("Проверка что ответ содержит данные инвентаря в правильном формате"):
            #assert response.json() == {"approved": 57, "delivered": 50}
            inventory_data = response.json()
            assert "approved" in inventory_data
            assert "delivered" in inventory_data

        with allure.step("Проверка типов данных и положительных значений"):
            assert isinstance(inventory_data["approved"], int) and inventory_data["approved"] >= 0
            assert isinstance(inventory_data["delivered"], int) and inventory_data["delivered"] >= 0




