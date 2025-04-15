#!/bin/sh
set -e

media_contents=$(ls -A /media 2>/dev/null || true)

echo $media_contents
if [ -z "$media_contents" ]; then
    echo "Directory /media is empty. Copying initial media files from /default_media..."
    cp -r /default_media /media
fi

cp -R /default_media/. /media/

exec minio server /media
