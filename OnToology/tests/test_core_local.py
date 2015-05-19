# 
# from OnToology.tests import LocalRepoTestCase
# 
# from OnToology import views
# import mimic_webhook
# 
# 
# class TestCoreLocalCycle(LocalRepoTestCase):
# #     def __init__(self):
# #         #LocalRepoTestCase.__init__()
# #         super( LocalRepoTestCase, self ).__init__()
#         
# #     def setUp(self):
# #         super(LocalRepoTestCase,self).setUp()
# 
#     def test_webhook(self):
#         self.addWebhook()
#     
#     def test_collaborator(self):
#         self.addCollaborator()
#         
#     def test_full_cycle(self):# add assert, I can use log files to validate this
#         request = mimic_webhook.get_fake_webhook_ontology_change_request(self.test_repo, self.username)
#         views.add_hook(request)
#     
#     
#     def tearDown(self):
#         LocalRepoTestCase.tearDown(self)
#         self.removeWebhook()
#         self.removeCollaborator()
#         
#         
# 
#                     
# 
#         
#         
