from nectar import ec2_conn

s_grps = ec2_conn.get_all_security_groups()

for grp in s_grps:
    print('S/Group id: {}, S/Group name: {}'.format(grp.id, grp.name))
