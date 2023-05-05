FROM ghcr.io/napari/napari-xpra AS napari-xpra

RUN python3 -m pip install btrack cellpose zmq pillow openai regex 
RUN python3 -m pip install git+https://github.com/benlansdell/napari-ethome.git

COPY napari-image-pipeline-dev /napari-image-pipeline-dev
RUN python3 -m pip install napari-accelerated-pixel-and-object-classification
RUN python3 -m pip install -e napari-image-pipeline-dev

COPY Napari_plugin_for_workflow_design /Napari_plugin_for_workflow_design
RUN python3 -m pip install -e Napari_plugin_for_workflow_design

ENV DISPLAY=:100
ENV XPRA_PORT=9876
ENV XPRA_START="python3 -m napari"
ENV XPRA_EXIT_WITH_CLIENT="yes"
ENV XPRA_XVFB_SCREEN="1920x1080x24+32"
EXPOSE 9876

CMD echo "Launching napari on Xpra. Connect via http://localhost:$XPRA_PORT"; \
    xpra start \
    --bind-tcp=0.0.0.0:$XPRA_PORT \
    --html=on \
    --start="$XPRA_START" \
    --exit-with-client="$XPRA_EXIT_WITH_CLIENT" \
    --daemon=no \
    --xvfb="/usr/bin/Xvfb +extension Composite -screen 0 $XPRA_XVFB_SCREEN -nolisten tcp -noreset" \
    --pulseaudio=no \
    --notifications=no \
    --bell=no \
    $DISPLAY

ENTRYPOINT []