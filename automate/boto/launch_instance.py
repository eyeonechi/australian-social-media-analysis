from nectar import ec2_conn

# ec2_conn.run_instances(image_id, key_name, instance_type, security_groups)
# Image Id: ami-00003837, image name: NeCTAR Ubuntu 16.04 LTS (Xenial) amd64
# so image_id sets ami-00003837 means Ubuntu 16.04 will be installed to the new instance.
reservation = ec2_conn.run_instances('ami-00003837', key_name='sakuya',
                                     instance_type='m1.small', security_groups=['default'])
instance = reservation.instances[0]
print('New instance {} has been created.'.format(instance.id))
