import boto
from boto.ec2.regioninfo import RegionInfo


region = RegionInfo(name='melbourne', endpoint='nova.rc.nectar.org.au')
ec2_conn = boto.connect_ec2(aws_access_key_id='357d606b238949c7991485e8b587cc5e',
                            aws_secret_access_key='3ab78559fb8f4310890c37abfa610448',
                            is_secure=True,
                            region=region,
                            port=8773,
                            path='/Services/Cloud',
                            validate_certs=False)
