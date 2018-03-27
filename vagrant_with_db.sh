# This is to allow the guest to access the host DB
vagrant up
vagrant ssh -- -R 27017:localhost:27017
