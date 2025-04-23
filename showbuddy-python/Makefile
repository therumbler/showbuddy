
.PHONY: build-docker run-docker run-local

IMAGE_NAME = ${USER}/showbuddy-docker

build-docker:
	echo "building $IMAGE_NAME"
 	# docker rmi $(docker images --filter=reference="*IMAGE_NAME*" -q)
	docker build -t ${IMAGE_NAME} .

run-docker: build-docker
	docker run -p 8000:8000 -e SPREADLY_API_KEY="${SPREADLY_API_KEY}" ${IMAGE_NAME}

run-local:
	./entrypoint.sh