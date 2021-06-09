app=lemon
cqhttp=go-cqhttp

$(app): abort-$(app)
	docker run -dp 0.0.0.0:6000:6000 -v $(PWD)/src/data/store:/app/src/data/store --name $(app) $(app):latest
cqhttp: abort-cqhttp
	cd cqhttp && \
	chmod +x $(cqhttp) && \
	./$(cqhttp) > /dev/null 2>&1 &
start:
	make cqhttp
	make $(app)
commit:
	git add src/data/store
	if [ -n "`git status | grep 'Changes to be committed'`" ]; then \
  		git commit -m 'save stored'; \
	fi
	git add .
	if [ -z "`git stash | grep 'No local changes to save'`" ]; then git stash drop; fi
	git pull origin master
	if [ -z "`git status | grep 'is up to date'`" ]; then git push origin master; fi
upgrade:
	make commit
	if [ -z "`docker images | grep python | grep 3.8`" ]; then docker pull python:3.8; fi
	docker build -t $(app):latest .
	make $(app)

abort: abort-cqhttp abort-$(app)
abort-$(app):
	if [ -n "`docker ps -a | grep $(app)`" ]; then docker rm `docker stop $(app)`; fi
abort-cqhttp:
	if [ -n "`pgrep $(cqhttp)`" ]; then kill `pgrep $(cqhttp)`; fi

.PHONY: cqhttp upgrade start abort abort-$(app) abort-cqhttp
