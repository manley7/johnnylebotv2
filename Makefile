.PHONY: clean train-nlu train-core cmdline server

TEST_PATH=./

help:
	@echo "    clean"
	@echo "        Remove python artifacts and build artifacts."
	@echo "    train-nlu"
	@echo "        Trains a new nlu model using the projects Rasa NLU config"
	@echo "    train-core"
	@echo "        Trains a new dialogue model using the story training data"
	@echo "    action-server"
	@echo "        Starts the server for custom action."

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f  {} +
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf docs/_build

train-nlu:
	python -m rasa_nlu.train -c nlu_config.yml --data data/model-banque.json -o models --fixed_model_name nlu --project current --verbose

	python -m rasa_nlu.server --path C:\Users\FR019136\Documents\SmartAutomation\starter-pack-rasa-stack-master\models\modelbanque -c C:\Users\FR019136\Documents\SmartAutomation\starter-pack-rasa-stack-master\nlu_config.yml --port 5001 
	curl -XPOST localhost:5001/train?project=fr_model_doc -d @C:\Users\FR019136\Documents\SmartAutomation\starter-pack-rasa-stack-master\data\model-banque.json -H "Content-Type: application/json" 
	
train-core:
	python -m rasa_core.train -d domain_banque_final.yml -s data/stories_banque_final.md -o models/banque_final/dialogue --epochs 200

cmdline:
	python -m rasa_core.run -d models/current/dialogue -u models/current/nlu --endpoints endpoints.yml

action-server:
	python -m rasa_core_sdk.endpoint --actions actions

	python -m rasa_core.run --enable_api -d models/current/dialogue -u models/current/nlu -o out.log

	curl -XPOST localhost:5005/conversations/default/respond -d '{"query":"j'ai perdu ma carte bancaire"}' | python -mjson.tool
	curl -XPOST http://localhost:5005/conversations/default/tracker/events -d '{"event": "slot", "name": "cuisine", "value": "mexican"}'

	python -m rasa_core.run -d models/current/dialogue -u models/current/nlu --port 5002 -c telegram --credentials telegram_credentials.yml

	python -m rasa_core.run -d models/current/dialogue -u models/current/nlu --port 5005 --credentials credentials.yml

	python -m rasa_core.run -d models/banque_final/dialogue -u models/banque_final/nlu --port 5002 -c telegram --credentials telegram_credentials.yml