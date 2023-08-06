from devops_requests import grafana
import unittest
import json
import os
import shutil
import sys


TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), 'test_files')
DASHBOARDS_DIR = os.path.join(TEST_FILES_DIR, 'dashboards')
DASHBOARD_PATH = os.path.join(DASHBOARDS_DIR, 'dashboard.json')
NOTIFICATION_CHANNELS_DIR = os.path.join(TEST_FILES_DIR, 'notification-channels')
NOTIFICATION_CHANNEL_PATH = os.path.join(NOTIFICATION_CHANNELS_DIR, 'notification-channel.json')
EXPORTED_FILES_DIR = os.path.join(TEST_FILES_DIR, 'exported')


class TestGrafana(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        grafana_url = os.environ.get('GRAFANA_URL')
        grafana_api_key = os.environ.get('GRAFANA_API_KEY')
        if grafana_url is None or grafana_api_key is None:
            raise RuntimeError('Must set GRAFANA_URL and GRAFANA_API_KEY environment variables')

        grafana.set_url(grafana_url)
        grafana.set_api_key(grafana_api_key)

        with open(DASHBOARD_PATH) as db_file, open(NOTIFICATION_CHANNEL_PATH) as nc_file:
            cls.test_dashboard = json.load(db_file)
            cls.test_notification_channel = json.load(nc_file)


    def tearDown(self):
        for db in grafana.list_dashboards():
            grafana.delete_dashboard(db['uid'])

        for nc in grafana.list_notification_channels():
            grafana.delete_notification_channel(nc['uid'])

        if os.path.exists(EXPORTED_FILES_DIR):
            shutil.rmtree(EXPORTED_FILES_DIR)

    
    ###############################################################################
    # Helpers
    ###############################################################################

    def create_test_dashboard(self):
        return grafana.create_dashboard(self.test_dashboard)


    def create_test_notification_channel(self):
        return grafana.create_notification_channel(self.test_notification_channel)


    ###############################################################################
    # API Request Tests
    ###############################################################################

    def test_make_request_no_url(self):
        url = grafana.grafana_url
        grafana.set_url('')
        with self.assertRaises(ValueError):
            grafana.make_request('alert-notifications', method='get')
        grafana.set_url(url)


    def test_make_request_no_api_key(self):
        api_key = grafana.api_key
        grafana.set_api_key('')
        with self.assertRaises(ValueError):
            grafana.make_request('alert-notifications', method='get')
        grafana.set_api_key(api_key)


    def test_make_request_invalid_method(self):
        with self.assertRaises(ValueError):
            grafana.make_request('alert-notifications', method='garbage')
    

    ###############################################################################
    # Dashboard Tests
    ###############################################################################

    def test_search_dashboards(self):
        uid = self.create_test_dashboard()
        dbs = grafana.search_dashboards(query=self.test_dashboard['title'])
        found = any( db for db in dbs if db['uid'] == uid )
        self.assertTrue(found)


    def test_search_dashboards_nonexistent(self):
        dbs = grafana.search_dashboards(query='garbage')
        self.assertEqual(dbs, [])


    def test_list_dashboards(self):
        self.create_test_dashboard()
        dbs = grafana.list_dashboards()
        self.assertNotEqual(dbs, [])


    def test_list_dashboards_none(self):
        dbs = grafana.list_dashboards()
        self.assertEqual(dbs, [])


    def test_get_dashboard(self):
        uid = self.create_test_dashboard()
        dashboard = grafana.get_dashboard(uid)
        self.assertIsNotNone(dashboard)
        self.assertEqual(dashboard['uid'], uid)


    def test_get_dashboard_nonexistent(self):
        dashboard = grafana.get_dashboard('garbage')
        self.assertIsNone(dashboard)

    
    def test_get_dashboard_by_name(self):
        uid = self.create_test_dashboard()
        db = grafana.get_dashboard_by_name(self.test_dashboard['title'])
        self.assertIsNotNone(db)
        self.assertEqual(uid, db['uid'])


    def test_get_dashboard_by_name_nonexistent(self):
        db = grafana.get_dashboard_by_name('garbage')
        self.assertIsNone(db)


    def test_create_dashboard(self):
        uid = grafana.create_dashboard(self.test_dashboard)
        self.assertIsNotNone(uid)
        db = grafana.get_dashboard(uid)
        self.assertIsNotNone(db)

    
    def test_create_dashboard_keep_uid(self):
        uid = grafana.create_dashboard(self.test_dashboard, keep_uid=True)
        self.assertEqual(uid, self.test_dashboard['uid'])
        db = grafana.get_dashboard(uid)
        self.assertIsNotNone(db)
        self.assertEqual(db['uid'], self.test_dashboard['uid'])


    def test_create_dashboard_invalid(self):
        invalid_db = {
            'bogus': 'garbage'
        }

        with self.assertRaises(Exception):
            grafana.create_dashboard(invalid_db)


    def test_delete_dashboard(self):
        uid = self.create_test_dashboard()
        self.assertIsNotNone(grafana.get_dashboard(uid))
        self.assertTrue(grafana.delete_dashboard(uid))
        self.assertIsNone(grafana.get_dashboard(uid))


    def test_delete_dashboard_nonexistent(self):
        self.assertFalse(grafana.delete_dashboard('garbage'))


    def test_import_dashboard(self):
        uid = grafana.import_dashboard(DASHBOARD_PATH)
        self.assertIsNotNone(uid)
        self.assertIsNotNone(grafana.get_dashboard(uid))


    def test_import_dashboard_nonexistent(self):
        nonexistent_file_path = os.path.join(DASHBOARDS_DIR, 'nonexistent.json')
        with self.assertRaises(Exception):
            grafana.import_dashboard(nonexistent_file_path)


    def test_import_dashboards(self):
        num_files = len(os.listdir(DASHBOARDS_DIR))
        uids = grafana.import_dashboards(DASHBOARDS_DIR)
        self.assertEqual(len(uids), num_files)
        for uid in uids:
            self.assertIsNotNone(grafana.get_dashboard(uid))


    def test_import_dashboards_nonexistent_dir(self):
        with self.assertRaises(Exception):
            grafana.import_dashboards('garbage')


    def test_export_dashboard(self):
        uid = self.create_test_dashboard()
        imported_dashboard = grafana.get_dashboard(uid)

        filename = 'exported_dashboard.json'
        filepath = os.path.join(EXPORTED_FILES_DIR, filename)
        grafana.export_dashboard(uid, filepath)

        self.assertTrue(os.path.exists(filepath))
        with open(filepath, 'r') as exported_file:
            exported_dashboard = json.load(exported_file)
        
        self.assertEqual(exported_dashboard, imported_dashboard)


    def test_export_dashboard_nonexistent(self):
        with self.assertRaises(ValueError):
            filepath = os.path.join(EXPORTED_FILES_DIR, 'garbage.json')
            grafana.export_dashboard('garbage', filepath)


    def test_export_all_dashboards(self):
        self.create_test_dashboard()
        all_dashboard_uids = [ result['uid'] for result in grafana.list_dashboards() ]
        all_dashboards = [ grafana.get_dashboard(uid) for uid in all_dashboard_uids ]

        grafana.export_all_dashboards(EXPORTED_FILES_DIR)

        exported_dashboards = []
        for filename in os.listdir(EXPORTED_FILES_DIR):
            filepath = os.path.join(EXPORTED_FILES_DIR, filename)
            with open(filepath, 'r') as exported_file:
                exported_dashboard = json.load(exported_file)
                exported_dashboards.append(exported_dashboard)

        for dashboard in all_dashboards:
            self.assertIn(dashboard, exported_dashboards)
        

    ###############################################################################
    # Notification Channel Tests
    ###############################################################################

    def test_list_notification_channels(self):
        self.create_test_notification_channel()
        channels = grafana.list_notification_channels()
        self.assertNotEqual(channels, [])


    def test_list_notification_channels_none(self):
        self.assertEqual([], grafana.list_notification_channels())


    def test_get_notification_channel(self):
        uid = self.create_test_notification_channel()
        channel = grafana.get_notification_channel(uid)
        self.assertIsNotNone(channel)
        self.assertEqual(uid, channel['uid'])


    def test_get_notification_channel_nonexistent(self):
        channel = grafana.get_notification_channel('garbage')
        self.assertIsNone(channel)


    def test_get_notification_channel_by_name(self):
        uid = self.create_test_notification_channel()
        found = grafana.get_notification_channel_by_name(self.test_notification_channel['name'])
        self.assertIsNotNone(found)
        self.assertEqual(uid, found['uid'])


    def test_get_notification_channel_by_name_nonexistent(self):
        found = grafana.get_notification_channel_by_name('garbage')
        self.assertIsNone(found)


    def test_create_notification_channel(self):
        uid = grafana.create_notification_channel(self.test_notification_channel)
        self.assertIsNotNone(uid)
        created = grafana.get_notification_channel(uid)
        self.assertIsNotNone(created)
        self.assertEqual(uid, created['uid'])


    def test_create_notification_channel_keep_uid(self):
        original_uid = self.test_notification_channel['uid']
        assigned_uid = grafana.create_notification_channel(self.test_notification_channel, keep_uid=True)
        self.assertIsNotNone(assigned_uid)
        self.assertEqual(assigned_uid, original_uid)


    def test_create_notification_channel_invalid(self):
        invalid_channel = {
            'bogus': 'garbage'
        }

        with self.assertRaises(Exception):
            grafana.create_notification_channel(invalid_channel)


    def test_delete_notification_channel(self):
        uid = self.create_test_notification_channel()
        self.assertIsNotNone(grafana.get_notification_channel(uid))
        self.assertTrue(grafana.delete_notification_channel(uid))
        self.assertIsNone(grafana.get_notification_channel(uid))


    def test_delete_notification_channel_nonexistent(self):
        self.assertFalse(grafana.delete_notification_channel('garbage'))


    def test_import_notification_channel(self):
        uid = grafana.import_notification_channel(NOTIFICATION_CHANNEL_PATH)
        self.assertIsNotNone(uid)
        self.assertIsNotNone(grafana.get_notification_channel(uid))


    def test_import_notification_channel_nonexistent(self):
        with self.assertRaises(Exception):
            grafana.import_notification_channel('garbage')


    def test_import_notification_channels(self):
        num_files = len(os.listdir(NOTIFICATION_CHANNELS_DIR))
        uids = grafana.import_notification_channels(NOTIFICATION_CHANNELS_DIR)
        self.assertEqual(len(uids), num_files)
        for uid in uids:
            self.assertIsNotNone(grafana.get_notification_channel(uid))


    def test_import_notification_channels_nonexistent_dir(self):
        with self.assertRaises(Exception):
            grafana.import_notification_channels('garbage')


    def test_export_notification_channel(self):
        uid = self.create_test_notification_channel()
        imported = grafana.get_notification_channel(uid)

        filename = 'exported-notification-channel.json'
        filepath = os.path.join(EXPORTED_FILES_DIR, filename)
        grafana.export_notification_channel(uid, filepath)

        self.assertTrue(os.path.exists(filepath))
        with open(filepath) as exported_file:
            exported = json.load(exported_file)

        self.assertEqual(exported, imported)


    def test_export_notification_channel_nonexistent(self):
        with self.assertRaises(Exception):
            filepath = os.path.join(EXPORTED_FILES_DIR, 'garbage.json')
            grafana.export_notification_channel('garbage', filepath)


    def test_export_all_notification_channels(self):
        self.create_test_notification_channel()
        all_notification_channel_uids = [ result['uid'] for result in grafana.list_notification_channels() ]
        all_notification_channels = [ grafana.get_notification_channel(uid) for uid in all_notification_channel_uids ]

        grafana.export_all_notification_channels(EXPORTED_FILES_DIR)

        exported_notification_channels = []
        for filename in os.listdir(EXPORTED_FILES_DIR):
            filepath = os.path.join(EXPORTED_FILES_DIR, filename)
            with open(filepath, 'r') as exported_file:
                exported_notification_channel = json.load(exported_file)
                exported_notification_channels.append(exported_notification_channel)

        for notification_channel in all_notification_channels:
            self.assertIn(notification_channel, exported_notification_channels)



if __name__ == "__main__":
    unittest.main()