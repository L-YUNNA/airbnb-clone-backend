#from django.test import TestCase
from rest_framework.test import APITestCase
from . import models

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
        response = self.client.post(self.URL)  # 아무 데이터도 보내지 않음 (그러나 Amenity 모델에서 name 필드는 필수 항목임)
        data = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("name", data)



        

        

        
        
