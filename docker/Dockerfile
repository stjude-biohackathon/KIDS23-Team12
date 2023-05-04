FROM ghcr.io/napari/napari-xpra AS napari-xpra

RUN python3 -m pip install btrack cellpose

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
