build:
	pip freeze > requirements.txt
	sam build && sam package --profile maxi80

deploy:
	sam deploy --profile maxi80

test:
	python -m unittest tests.test_handler.TestMaxi80Backend 

testsam:
	sam local invoke -e ./tests/event.json --env-vars ./tests/env.json

package:
	sam package --profile maxi80 --resolve-s3 