#!/bin/zsh
for i in {001..042}
do
  s3cmd get s3://arxiv/src/arXiv_src_1904_$i.tar --requester-pays
done