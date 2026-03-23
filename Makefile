build:
	pip freeze > requirements.txt
	sam build && sam package --profile maxi80

deploy:
	sam deploy --profile maxi80

test:
	python -m pytest tests/ -v

testsam:
	sam local invoke -e ./tests/event.json --env-vars ./tests/env.json

package:
	sam package --profile maxi80 --resolve-s3 

logs:
	sam logs --stack-name Maxi80Backend --profile maxi80 --region eu-west-1 --tail
