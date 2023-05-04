dockerbuild:
		docker build -t hub-napari-xpra .

dockerpush:
		docker image tag hub-napari-xpra:latest benlansdell/hub-napari-xpra:latest
		docker image push benlansdell/hub-napari-xpra:latest

dockerpull:
		docker pull benlansdell/hub-napari-xpra:latest