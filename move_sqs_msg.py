  import json
  import time
  import argparse
  import boto.sqs

  from termcolor import cprint

  parser = argparse.ArgumentParser(description="Move messages from one SQS queue to another.")
  parser.add_argument('-s', '--src', required=True,
                      help='Name of source queue.')
  parser.add_argument('-d', '--dst', required=True,
                      help='Name of destination queue.')
  parser.add_argument('--region', default='us-east-1',
                      help='AWS region of both the queues (default: \'us-east-1\').')
  parser.add_argument('--profile', default='comet-test',
                          help='The AWS profile name containing credentials. Credentials are usually located in \'~/.aws/credentials\' file')
  args = parser.parse_args()

  conn = boto.sqs.connect_to_region(
            args.region,
            profile_name=args.profile
    )

  q = conn.get_queue(args.src)
  qto = conn.get_queue(args.dst)

  from boto.sqs.message import RawMessage

  import time
  while(True):
          for m in q.get_messages():
                  # print '%s: %s' % (m, m.get_body())
                  me = RawMessage()
                  me.set_body(m.get_body())
                  retval = qto.write(me)
                  print 'added message %s, got retval: %s' % (me.get_body(),retval)
                  q.delete_message(m)
          time.sleep(1)
