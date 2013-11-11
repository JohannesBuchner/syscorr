#!/bin/bash

python gen.py

# these take quite a bit of time.

RESUME=1 python analyse.py out/sysline_ sysline/chain?? &
#RESUME=1 python analyse.py out/random_ random/chain?? &

wait

for i in out/sysline_*post_model_data.pdf; do xdg-open $i; done

