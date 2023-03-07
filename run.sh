docker run -iPt \
    --rm \
    -v /dev/bus/usb:/dev/bus/usb \
    -v /dev/input:/dev/input \
    -p 8000:8000 \
    --env="DISPLAY=$DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    --volume="$XAUTHORITY:$XAUTHORITY" \
    --env="XAUTHORITY=$XAUTHORITY" \
    --runtime=nvidia \
    --name="nlp_case" \
    --privileged \
    chipix \

