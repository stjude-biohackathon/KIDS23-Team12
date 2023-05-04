dockerbuild:
		docker build -t hub-napari-xpra .

dockerpush:
		docker image tag hub-napari-xpra:latest svlpdocker01.stjude.org:443/hub-napari-xpra:latest
		docker image push svlpdocker01.stjude.org:443/hub-napari-xpra:latest

dockerpull:
		docker pull svlpdocker01.stjude.org:443/hub-napari-xpra:latest