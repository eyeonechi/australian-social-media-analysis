import boto
from boto.ec2.regioninfo import RegionInfo


class Nectar:

    def __init__(self):
        region = RegionInfo(name='melbourne', endpoint='nova.rc.nectar.org.au')
        self.ec2_conn = boto.connect_ec2(aws_access_key_id='357d606b238949c7991485e8b587cc5e',
                                         aws_secret_access_key='3ab78559fb8f4310890c37abfa610448',
                                         is_secure=True,
                                         region=region,
                                         port=8773,
                                         path='/Services/Cloud',
                                         validate_certs=False)

    def add_instance(self, type):
        if type == "DATABASE":
            reservation = self.ec2_conn.run_instances('ami-00003837', key_name='sakuya',
                                                      instance_type='m2.medium',
                                                      security_groups=['default', 'ssh', 'couchDB'],
                                                      placement='melbourne-qh2')
            instance = reservation.instances[0]
            return {"id": instance.id, "ip": instance.private_ip_address}
        elif type == "HARVESTER":
            reservation = self.ec2_conn.run_instances('ami-00003837', key_name='sakuya',
                                                      instance_type='m2.medium',
                                                      security_groups=['default', 'ssh', 'xserver'],
                                                      placement='melbourne-qh2')
            instance = reservation.instances[0]
            return {"id": instance.id, "ip": instance.private_ip_address}

    def list_instances(self):
        reservations = self.ec2_conn.get_all_instances()
        res = []

        for reservation in reservations:
            res.append({"id": reservation.instances[0].id, "ip": reservation.instances[0].private_ip_address})
        return res

    def list_image(self):
        images = self.ec2_conn.get_all_images()
        res = []
        for img in images:
            res.append({"id": img.id, "name": img.name})
        return res

    def list_security_group(self):
        s_grp = self.ec2_conn.get_all_security_groups()
        res = []
        for grp in s_grp:
            res.append({"id": grp.id, "name": grp.name})
        return res


if __name__ == "__main__":
    nectar = Nectar()
