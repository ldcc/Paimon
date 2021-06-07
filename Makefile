nb=nb
cqhttp=go-cqhttp

paimon: abort-paimon
	$(nb) run >> logs/$(shell date +"%Y-%m-%d").log 2>&1 &
	#docker run -dp 0.0.0.0:6000:6000 -v $(PWD)/src/data/store:/app/src/data/store --name paimon paimon:latest
cqhttp: abort-cqhttp
	cd cqhttp && \
	chmod +x $(cqhttp) && \
	./$(cqhttp) > /dev/null 2>&1 &
start:
	make cqhttp
	make paimon
commit:
	git add src/data/store
	git commit -m 'save stored'
	git push origin master
	git stash
	git stash drop
upgrade:
	make commit
	git pull origin master
	python3.8 -m pip install -r requirements.txt
	#docker build -t paimon:latest .
	make start

abort: abort-cqhttp abort-paimon
abort-paimon:
	$(shell if [ -n "pgrep $(nb)" ]; then sudo pkill $(nb); fi)
	#docker stop paimon
	#docker container rm paimon
abort-cqhttp:
	$(shell if [ -n "pgrep $(cqhttp)" ]; then sudo pkill $(cqhttp); fi)

.PHONY: cqhttp upgrade start abort abort-paimon abort-cqhttp
