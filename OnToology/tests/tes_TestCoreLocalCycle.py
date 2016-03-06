#
# from OnToology.tests.LocalRepoTestClass import LocalRepoTestCase
#
# from OnToology import views
# import mimic_webhook
#
# from mongoengine import connect
#
# from OnToology import settings
#
# class TestCoreLocalCycle(LocalRepoTestCase):
#
#
# #     def test_clean_things_first(self):
# #         self.removeWebhook()
# #         self.removeCollaborator()
#
#
#     def test_webhook(self):
#         self.addWebhook()
#
#     def test_collaborator(self):
#         self.addCollaborator()
#
#     def test_full_cycle(self):# add assert, I can use log files to validate this
#         print 'test_repo: '+self.test_repo
#         request = mimic_webhook.get_fake_webhook_ontology_change_request(self.test_repo, self.username)
#         connect('OnToology')
#         views.add_hook(request)
#         #views.add_hook_for_tests(request)
#
# #     def tearDown(self):
# #         LocalRepoTestCase.tearDown(self)
# #         self.removeWebhook()
# #         self.removeCollaborator()
#
#
#
#
#
#
#
