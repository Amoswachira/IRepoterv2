import unittest
import json
from app import create_app
from ....api.v2.models import Model
app = create_app()
database = Model()

HEADERS = {'Content-Type': 'application/json'}
URL_REDFLAGS = "/api/v2/interventions"
URL_REDFLAGS_ID = "/api/v2/intervention/2"
URL_REDFLAGS_IDD = "/api/v2/intervention/5"
URL_REDFLAGS_IDS = "/api/v2/intervention/1168878781"
URL_LOCATION = "/api/v2/interventions/3/location"
URL_COMMENT = "/api/v2/interventions/4/comment"
URL_REDSTATUS = "/api/v2/interventions/6/status-red"
URL_INTESTATUS = "/api/v2/interventions/7/status"


class RedFlagTestCase(unittest.TestCase):

    def setUp(self):
        database.drop_tables()
        database.create_tables()
        app.testing = True
        self.app = create_app()
        self.client = self.app.test_client()
        self.data = {
            "id": "1",
            "type": "Redflag",
            "location": "naxs",
            "Images": "Images",
            "Videos": "Videos",
            "comment": "df"
        }
        self.data2 = {
            "id": "2",
            "type": "Redflag",
            "location": "naxs",
            "Images": "Images",
            "Videos": "Videos",
            "comment": "df"
        }
        self.data3 = {
            "id": "3",
            "type": "Intervention",
            "location": "naxs",
            "Images": "Images",
            "Videos": "Videos",
            "comment": "df",
            "status": "draft"
        }
        self.data4 = {
            "id": "4",
            "type": "Redflag",
            "location": "naxs",
            "Images": "Images",
            "Videos": "Videos",
            "comment": "df",
            "status": "draft"
        }
        self.data5 = {
            "id": "5",
            "type": "Redflag",
            "location": "naxs",
            "Images": "Images",
            "Videos": "Videos",
            "comment": "df"
        }
        self.data6 = {
            "id": "6",
            "type": "Redflag",
            "location": "naxs",
            "Images": "Images",
            "Videos": "Videos",
            "comment": "df",
            "status": "draft"
        }
        self.data7 = {
            "id": "7",
            "type": "Intervention",
            "location": "naxs",
            "Images": "Images",
            "Videos": "Videos",
            "comment": "df",
            "status": "draft"
        }
        self.redflagpatch = {
            "type": "Redflag",
            "isAdmin": "True",
            "status": "under investigation"
        }
        self.interventionpatch = {
            "type": "Intervention",
            "isAdmin": "True",
            "status": "under investigation"
        }

    def test_get_redflags(self):
        response = self.client.get(URL_REDFLAGS)
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_post_redflag(self):
        response = self.client.post(
            URL_REDFLAGS, headers=HEADERS, data=json.dumps(self.data)
        )
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Created intervention record', str(result))
    
    def test_get_one_redflag(self):
        response = self.client.post(
            URL_REDFLAGS, headers=HEADERS, data=json.dumps(self.data2)
        )
        response2 = self.client.get(URL_REDFLAGS_ID)
        result = json.loads(response2.data)
        self.assertEqual(response2.status_code, 200)

    def test_redflag_not_found(self):
        response = self.client.get(URL_REDFLAGS_IDS)
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertIn("intervention record does not exist.", str(result))
    
    def test_update_location_of_one_redflag(self):
        response = self.client.post(
            URL_REDFLAGS, headers=HEADERS, data=json.dumps(self.data3)
        )
        response2 = self.client.patch(
            URL_LOCATION, headers=HEADERS, data=json.dumps({
                "location": "Kisumu"
            })
        )
        result = json.loads(response2.data)
        self.assertEqual(response2.status_code, 200)
        self.assertIn("Updated intervention's location", str(result))

    def test_update_comment_of_one_redflag(self):
        response = self.client.post(
            URL_REDFLAGS, headers=HEADERS, data=json.dumps(self.data4)
        )
        response2 = self.client.patch(
            URL_COMMENT, headers=HEADERS, data=json.dumps({
                "comment": "curruption"
            })
        )
        result = json.loads(response2.data)
        self.assertEqual(response2.status_code, 200)
        self.assertIn("Updated intervention's comment", str(result))
    
    def test_update_redflag_status(self):
        response = self.client.post(
            URL_REDFLAGS, headers=HEADERS, data=json.dumps(self.data6)
        )
        response2 = self.client.patch(
            URL_REDSTATUS, headers=HEADERS, data=json.dumps(
                self.redflagpatch
            )
        )
        result = json.loads(response2.data)
        self.assertEqual(response2.status_code, 200)
        self.assertIn("Updated redflag record status", str(result))

    def test_update_intervention_status(self):
        response = self.client.post(
            URL_REDFLAGS, headers=HEADERS, data=json.dumps(self.data7)
        )
        response2 = self.client.patch(
            URL_INTESTATUS, headers=HEADERS, data=json.dumps(
                self.interventionpatch
            )
        )
        result = json.loads(response2.data)
        self.assertEqual(response2.status_code, 200)
        self.assertIn("Updated intervention record status", str(result))
    
    def test_delete_one_redflag(self):
        response = self.client.post(
            URL_REDFLAGS, headers=HEADERS, data=json.dumps(self.data5)
        )
        response2 = self.client.delete(URL_REDFLAGS_IDD)
        result = json.loads(response2.data)
        self.assertEqual(response2.status_code, 200)
        self.assertIn('Intervention record has been deleted', str(result))

    database.drop_tables()


if __name__ == "__main__":
    unittest.main()