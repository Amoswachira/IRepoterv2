"""unittests"""
import unittest
import json
from app import create_app
from ....api.v2.models import Model
app = create_app()
database = Model()


URL_REDFLAGS = "/api/v2/interventions"
URL_REDFLAGS_ID = "/api/v2/intervention/1"
URL_REDFLAGS_IDD = "/api/v2/intervention/1"
URL_REDFLAGS_IDS = "/api/v2/intervention/1168878781"
URL_LOCATION = "/api/v2/interventions/1/location"
URL_COMMENT = "/api/v2/interventions/1/comment"
URL_REDSTATUS = "/api/v2/redflag/1/status"
URL_INTESTATUS = "/api/v2/interventions/1/status"
URL_SIGNUP = "/api/v2/auth/signup"


class RedFlagTestCase(unittest.TestCase):
    """class methods for testing"""
    def setUp(self):
        database.drop_tables()
        database.create_tables()
        app.testing = True
        self.app = create_app()
        self.client = self.app.test_client()
        self.data = {
            "type": "Redflag",
            "location":"-1.59,67.8",
            "Images": "Images",
            "Videos": "Videos",
            "comment": "df"
        }
        self.data2 = {
            "type": "Redflag",
            "location":"-1.59,67.8",
            "Images": "Images",
            "Videos": "Videos",
            "comment": "df"
        }
        self.data3 = {
            "type": "Intervention",
            "location": "-1.59,67.8",
            "Images": "Images",
            "Videos": "Videos",
            "comment": "df",
            "status": "draft"
        }
        self.data4 = {
            "type": "Redflag",
            "location": "-1.59,67.8",
            "Images": "Images",
            "Videos": "Videos",
            "comment": "df",
            "status": "draft"
        }
        self.data5 = {
            "type": "Redflag",
            "location": "-1.59,67.8",
            "Images": "Images",
            "Videos": "Videos",
            "comment": "df"
        }
        self.data6 = {
            "type": "Redflag",
            "location": "-1.59,67.8",
            "Images": "Images",
            "Videos": "Videos",
            "comment": "df",
            "status": "draft"
        }
        self.data7 = {
            "type": "Intervention",
            "location": "-1.59,67.8",
            "Images": "Images",
            "Videos": "Videos",
            "comment": "df",
            "status": "draft"
        }
        self.redflagpatch = {
            "type": "Redflag",
            "status": "under investigation"
        }
        self.interventionpatch = {
            "type": "Intervention",
            "status": "under investigation"
        }
        self.user = {
            "firstname": "Admin",
            "lastname": "Admin",
            "othername": "Admin",
            "email": "Admin@gmail.com",
            "phoneNumber": "123456789",
            "username": "Admin",
            "password": "Admin"
            
        }

        response = self.client.post(
            URL_SIGNUP, data=json.dumps(self.user), headers={'Content-Type': 'application/json'})
        result = json.loads(response.data)
        self.token = result['data'][0]['token']
        self.access = "Bearer {}".format(self.token)
        self.assertEqual(response.status_code, 201)

    def test_get_redflags(self):
        """test get method for getting interventions"""
        response = self.client.get(URL_REDFLAGS, headers={
                                   'Content-Type': 'application/json'
                                   , "Authorization": self.access})
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_post_redflag(self):
        """test the post method"""
        response = self.client.post(
            URL_REDFLAGS, headers={'Content-Type': 'application/json'
            , "Authorization": self.access}, data=json.dumps(self.data)
        )
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Created intervention record', str(result))

    def test_get_one_redflag(self):
        """"test method to get one record by id"""
        response = self.client.post(
            URL_REDFLAGS, headers={'Content-Type': 'application/json'
            , "Authorization": self.access}, data=json.dumps(self.data2)
        )
        response2 = self.client.get(URL_REDFLAGS_ID, headers={
                                    'Content-Type': 'application/json'
                                    , "Authorization": self.access})
        result = json.loads(response2.data)
        self.assertEqual(response2.status_code, 200)

    def test_redflag_not_found(self):
        """test for not found record"""
        response = self.client.get(URL_REDFLAGS_IDS, headers={
                                   'Content-Type': 'application/json'
                                   , "Authorization": self.access})
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertIn("intervention record does not exist.", str(result))

    def test_update_location_of_one_redflag(self):
        """test patch method for location"""
        response = self.client.post(
            URL_REDFLAGS, headers={'Content-Type': 'application/json'
            , "Authorization": self.access}, data=json.dumps(self.data3)
        )
        response2 = self.client.patch(
            URL_LOCATION, headers={'Content-Type': 'application/json'
            , "Authorization": self.access}, data=json.dumps({
                "location": "-1.59,67.8"
            })
        )
        result = json.loads(response2.data)
        self.assertEqual(response2.status_code, 200)
        self.assertIn("Updated intervention's location", str(result))

    def test_update_comment_of_one_redflag(self):
        """test patch method for comment field by id"""
        response = self.client.post(
            URL_REDFLAGS, headers={'Content-Type': 'application/json'
            , "Authorization": self.access}, data=json.dumps(self.data4)
        )
        response2 = self.client.patch(
            URL_COMMENT, headers={'Content-Type': 'application/json'
            , "Authorization": self.access}, data=json.dumps({
                "comment": "curruption"
            })
        )
        result = json.loads(response2.data)
        self.assertEqual(response2.status_code, 200)
        self.assertIn("Updated intervention's comment", str(result))

    def test_update_redflag_status(self):
        """test patch for redflag status"""
        response = self.client.post(
            URL_REDFLAGS, headers={'Content-Type': 'application/json'
            , "Authorization": self.access}, data=json.dumps(self.data6)
        )
        response2 = self.client.patch(
            URL_REDSTATUS, headers={'Content-Type': 'application/json'
            , "Authorization": self.access}, data=json.dumps(
                self.redflagpatch
            )
        )
        result = json.loads(response2.data)
        self.assertEqual(response2.status_code, 200)
        self.assertIn("Updated redflag record status", str(result))

    def test_update_intervention_status(self):
        """test patch for intervention status"""
        response = self.client.post(
            URL_REDFLAGS, headers={'Content-Type': 'application/json'
            , "Authorization": self.access}, data=json.dumps(self.data7)
        )
        response2 = self.client.patch(
            URL_INTESTATUS, headers={'Content-Type': 'application/json'
            , "Authorization": self.access}, data=json.dumps(
                self.interventionpatch
            )
        )
        result = json.loads(response2.data)
        self.assertEqual(response2.status_code, 200)
        self.assertIn("Updated intervention record status", str(result))

    def test_delete_one_redflag(self):
        """"test delete method of one redflag"""
        response = self.client.post(
            URL_REDFLAGS, headers={'Content-Type': 'application/json'
            , "Authorization": self.access}, data=json.dumps(self.data5)
        )
        response2 = self.client.delete(URL_REDFLAGS_IDD, headers={
                                       'Content-Type': 'application/json'
                                       , "Authorization": self.access})
        result = json.loads(response2.data)
        self.assertEqual(response2.status_code, 200)
        self.assertIn('Intervention record has been deleted', str(result))

    database.drop_tables()


if __name__ == "__main__":
    unittest.main()
