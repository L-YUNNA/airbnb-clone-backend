#from django.test import TestCase
from rest_framework.test import APITestCase
from . import models
import string, random

class TestAmenities(APITestCase):

    NAME = "Amenity Test"
    DESC = "Amenity Des"

    URL = "/api/v1/rooms/amenities/"

    def setUp(self):
        models.Amenity.objects.create(name=self.NAME, description=self.DESC)

    def test_all_amenities(self):

        response = self.client.get(self.URL)
        data = response.json()
        #print(data)

        self.assertEqual(
            response.status_code,
            200,
            "Status code isn't 200."
        )
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], self.NAME,)
        self.assertEqual(data[0]["description"], self.DESC,)

    def test_create_amenity(self):

        new_amenity_name = "New Amenity"
        new_amenity_description = "New Amenity desc."
        # 글자 수 150개 이상의 문자 생성
        string_pool = string.ascii_letters
        wrong_name = ""
        for i in range(155):
            wrong_name += random.choice(string_pool)

        # Amenity 하나 생성
        response = self.client.post(
            self.URL, 
            data={"name":new_amenity_name,
                   "description":new_amenity_description})
        
        # 잘 생성됐는지 확인
        data = response.json()

        self.assertEqual(
            response.status_code, 
            200, 
            "Not 200 status code"
            )
        self.assertEqual(
            data['name'],
            new_amenity_name
        )
        self.assertEqual(
            data['description'],
            new_amenity_description
        )
        
        # 어떠한 데이터를 보냈을 때, 에러 잘 나는지 확인
        response = self.client.post(self.URL)  # 아무 데이터도 보내지 않음 (Amenity 모델에서 name 필드는 필수 항목임)
        data = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("name", data)

        response = self.client.post(
            self.URL,
            data={"name":wrong_name,})  # 최대길이 150글자만 가능한 name에 150 이상을 준 경우
        data = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("name", data)

class TestAmenity(APITestCase):
    
    NAME = "Test Amenity"
    DESC = "Test Dsc"

    URL = "/api/v1/rooms/amenities/"
    
    def setUp(self):
        models.Amenity.objects.create(name=self.NAME, description=self.DESC)

    def test_amenity_not_fount(self):
        response = self.client.get(self.URL + str(2))
        self.assertEqual(
            response.status_code, 
            404
            )
    
    def test_get_amenity(self):

        response = self.client.get(self.URL + str(1))
        data = response.json()
        self.assertEqual(
            response.status_code, 
            200
            )
        self.assertEqual(
            data["name"],
            self.NAME,
        )
        self.assertEqual(
            data["description"],
            self.DESC
        )

    def test_put_amenity(self):

        new_amenity_name = "New Amenity"
        # 글자 수 150개 이상의 문자 생성
        string_pool = string.ascii_letters
        wrong_name = ""
        for i in range(155):
            wrong_name += random.choice(string_pool)

        response = self.client.put(
            self.URL + str(1), 
            data={"name":new_amenity_name,})
        data = response.json()

        self.assertEqual(
            response.status_code, 
            200, 
            "Not 200 status code"
            )
        self.assertEqual(
            data['name'],
            new_amenity_name
        )
        self.assertEqual(
            data['description'],
            self.DESC
        )

        response = self.client.put(
            self.URL + str(1),
            data={"name":wrong_name,}
            )  
        data = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("name", data)

    def test_delete_amenity(self):
        response = self.client.delete(self.URL + str(1))
        self.assertEqual(response.status_code, 204)




        

        

        
        
