py_prog=python3.8

paimon:
	$(py_prog) bot.py > /dev/null 2>&1 &
go-cqhttp:
	cd cqhttp && \
	./go-cqhttp > /dev/null 2>&1 &
upgrade: abort
	git pull
	make paimon
abort:
	if [ -n pgrep "$(py_prog)" ]; then pkill $(py_prog); fi

.PHONY: upgrade abort