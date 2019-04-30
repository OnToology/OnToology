docker image build -t ontoologydev:latest .
docker container run
    -e github_password="$github_password"
    -e client_id_login="$client_id_login"
    -e client_id_public="$client_id_public"
    -e client_id_private="$client_id_private"
    -e client_secret_login="$client_secret_login"
    -e client_secret_public="$client_secret_public"
    -e client_secret_private="$client_secret_private"
    -e test_user_token="$test_user_token"
    -e test_user_email="$test_user_email"
    --interactive --tty --rm --name ontoologydev ontoologydev:latest