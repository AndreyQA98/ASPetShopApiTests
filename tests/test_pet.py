import allure
import pytest
import jsonschema
import requests
from . schemas.pet_schema import PET_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("pet")
class TestPet:
    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):
        with allure.step("Отправка запроса на удаление несуществущего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстого содержимого ответа"):
            assert response.text == "Pet deleted", "Текст ошибки не совпал с ожидаемым"


    @allure.title("Попытка обновить несуществущего питомца")
    def test_update_nonexistent_pet(self):
        with allure.step("Отправка запроса на обновление несуществущего питомца"):
            payload = {
                "id": 9999,
                "name": "Non-existent Pet",
                "status": "available"
            }
            response = requests.put(url=f"{BASE_URL}/pet", json=payload)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстого содержимого ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Попытка получить информацию о несуществующем питомце")
    def test_get_information_nonexistent_pet(self):
        with allure.step("Отправка запроса на получение информации о несуществующем питомце"):
            response = requests.get(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстого содержимого ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Добавление нового питомца")
    def test_add_pet(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {
                "id": 1,
                "name": "Buddy",
                "status": "available"
            }

        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert response.status_code == 200
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json['id'] == payload['id'], "id питомца не совпадает с ожидаемым"
            assert response_json['name'] == payload['name'], "имя питомца не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "статус питомца не совпадает с ожидаемым"


    @allure.title("Добавление нового питомца с полными данными")
    def test_add_pet_complete_data(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {
              "id": 10,
                "name": "doggie",
                "category": {
                    "id": 1,
                    "name": "Dogs"
                },
                "photoUrls": ["string"],
                "tags": [{"id": 0, "name": "string"}],
                "status": "available"
            }

        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert response.status_code == 200
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json['id'] == payload['id'], "id питомца не совпадает с ожидаемым"
            assert response_json['name'] == payload['name'], "имя питомца не совпадает с ожидаемым"
            assert response_json['category']['id'] == payload['category']['id'], "ID категории питомца не совпадает с ожидаемым"
            assert response_json['category']['name'] == payload['category']['name'], "Название категории питомца не совпадает с ожидаемым"
            assert response_json['photoUrls'] == payload['photoUrls'], "фотоурлы питомца не совпадает с ожидаемым"
            assert response_json['tags'] == payload['tags'], "теги питомца не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "статус питомца не совпадает с ожидаемым"


    @allure.title("Получение информации о питомце по ID")
    def test_get_pet_by_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response = requests.get(f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа и данных питомца"):
            assert response.status_code == 200
            assert response.json()["id"] == pet_id

    @allure.title("Обновление информации о питомце")
    def test_update_information_pet(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Подготовка данных для обновления питомца"):
            update_data = {
                "id": pet_id,
                "name": "Buddy Updated",
                "status": "sold"
            }

        with allure.step("Отправка PUT запроса для обновления питомца"):
            response = requests.put(f"{BASE_URL}/pet", json=update_data)

        with allure.step("Проверка статуса ответа и данных питомца"):
            assert response.status_code == 200
            assert response.json()["id"] == pet_id

        with allure.step("Получение данных обновленного питомца из ответа"):
            updated_pet = response.json()

        with allure.step("Проверка что питомец обновлен с правильными данными"):
            assert update_data["id"] == pet_id
            assert update_data["name"] == "Buddy Updated", "Имя не обновлено."
            assert update_data["status"] == "sold", "Статус не обновлен."

    @allure.title("Удаление питомца по ID")
    def test_delete_pet_by_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response = requests.get(f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа и данных питомца"):
            assert response.status_code == 200
            assert response.json()["id"] == pet_id

        with allure.step("Отправка запроса на удаление питомца"):
            delete_response = requests.delete(f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка успешного удаления"):
            assert delete_response.status_code == 200

        with allure.step("Проверка что питомец действительно удален"):
            get_response_after_delete = requests.get(f"{BASE_URL}/pet/{pet_id}")
            assert get_response_after_delete.status_code == 404

    @allure.title("Получение списка питомцев по статусу")
    @pytest.mark.parametrize(
        "status, expected_status_code, expected_response_type",
        [
            ("available", 200, list),
            ("pending", 200, list),
            ("sold", 200, list),
            ("unavailable", 400, dict),
            ("", 400, dict),
         ]
    )
    def test_get_pets_by_status(self, status, expected_status_code, expected_response_type):
        with allure.step(f"Отправка запроса на получение питомцев по статусу {status}"):
            response = requests.get(f"{BASE_URL}/pet/findByStatus", params={"status": status})

        with allure.step("Проверка статуса ответа и формата данных"):
            assert response.status_code == expected_status_code
            assert isinstance(response.json(), expected_response_type)






