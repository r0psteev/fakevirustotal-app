.PHONY: web

build: api web
api: 
	cd ./faketotal && make build
web:
	cd ./web && make build