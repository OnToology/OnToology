from django.test.testcases import SerializeMixin

# This it to force the tests to run sequentially (while the default is to run them in parallel)
# This is needed as the tests are executed using the same repo and user
print("serializer")
class Serializer(SerializeMixin):
    lockfile = __file__

    # def setUp(self):
    #     if len(OUser.objects.all()) == 0:
    #         create_user()
    #     self.url = 'ahmad88me/ontoology-auto-test-no-res'
    #     self.user = OUser.objects.all()[0]
    #
    #     logger.debug("rabbit host in test: "+rabbit_host)
    #     num_of_msgs = get_pending_messages()
    #     logger.debug("test> number of messages in the queue is: " + str(num_of_msgs))
    #     delete_all_repos_from_db()

    # def setUp(self):
    #     pass
