#!/usr/bin/env python

# This script uploads a file to Amazon S3 using boto
# usage: python s3upload.py bucketname filepath access-key secret-key

import os, sys
import math
import boto


def upload_file(s3, bucketname, file_path):

        b = s3.get_bucket(bucketname)

        filename = os.path.basename(file_path)
        # k = b.new_key(filename)

        mp = b.initiate_multipart_upload(filename)

        source_size = os.stat(file_path).st_size
        bytes_per_chunk = 5000*1024*1024
        chunks_count = int(math.ceil(source_size / float(bytes_per_chunk)))

        for i in range(chunks_count):
                offset = i * bytes_per_chunk
                remaining_bytes = source_size - offset
                bytes = min([bytes_per_chunk, remaining_bytes])
                part_num = i + 1

                print "uploading part " + str(part_num) + " of " + str(chunks_count)

                with open(file_path, 'r') as fp:
                        fp.seek(offset)
                        mp.upload_part_from_file(fp=fp, part_num=part_num, size=bytes)

        if len(mp.get_all_parts()) == chunks_count:
                mp.complete_upload()
                print "upload_file done"
        else:
                mp.cancel_upload()
                print "upload_file failed"

if __name__ == "__main__":

        if len(sys.argv) != 5:
                print "usage: python s3upload.py bucketname filepath access-key secret-key"
                exit(0)

        bucketname = sys.argv[1]

        filepath = sys.argv[2]

        AWS_ACCESS_KEY_ID = sys.argv[3]

        AWS_SECRET_ACCESS_KEY = sys.argv[4]

        s3 = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

        upload_file(s3, bucketname, filepath)
