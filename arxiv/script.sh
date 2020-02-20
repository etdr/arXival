#!/bin/zsh
for i in {001..033}
do
  s3cmd get s3://arxiv/src/arXiv_src_1901_$i.tar --requester-pays
done