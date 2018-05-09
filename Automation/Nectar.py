"""
@Team info:
    CCC Team 42 (Melbourne)
    Hannah Ha   963370
    Lan Zhou    824371
    Zijian Wang 950618
    Ivan Chee   736901
    Duer Wang   824325
"""
import boto
from boto.ec2.regioninfo import RegionInfo
import time


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

    def add_instance(self):
        reservation = self.ec2_conn.run_instances('ami-00003837', key_name='sakuya',
                                                  instance_type='m1.medium',
                                                  security_groups=['default', 'ssh', 'couchDB',
                                                                   'http', 'flask', 'xserver'],
                                                  placement='melbourne-qh2')
        instance = reservation.instances[0]
        return {"id": instance.id, "ip": instance.private_ip_address, "state": instance.state}

    def list_instances(self):
        reservations = self.ec2_conn.get_all_instances()
        res = []

        for reservation in reservations:
            res.append({"id": reservation.instances[0].id,
                        "ip": reservation.instances[0].private_ip_address,
                        "state": reservation.instances[0].state})
        return res

    def list_image(self):
        images = self.ec2_conn.get_all_images()
        res = []
        for img in images:
            res.append({"id": img.id, "name": img.name})
        return res

    def list_volumes(self):
        volumes = self.ec2_conn.get_all_volumes()
        res = []
        for volume in volumes:
            res.append({"id": volume.id, "status": volume.status})
        return res

    def list_security_group(self):
        s_grp = self.ec2_conn.get_all_security_groups()
        res = []
        for grp in s_grp:
            res.append({"id": grp.id, "name": grp.name})
        return res

    def add_volume(self, instance_id):
        volume = self.ec2_conn.create_volume(size=50, zone="melbourne-qh2")
        info = self.get_volume_info(volume.id)
        while info["status"] != "available":
            print("Volume state: " + info["status"])
            time.sleep(3)
            info = self.get_volume_info(volume.id)
        successful = volume.attach(instance_id, "/dev/vdc")
        if successful:
            print("volume: " + volume.id + " set and bounded to /dev/vdc")
        else:
            print("ERROR: volume creating failed.")

    def get_instance_info(self, instance_id):
        insts = self.list_instances()
        for inst in insts:
            if inst["id"] == instance_id:
                return inst
        return None

    def get_volume_info(self, volume_id):
        volumes = self.list_volumes()
        for volume in volumes:
            if volume["id"] == volume_id:
                return volume
        return None


if __name__ == "__main__":
    nectar = Nectar()
    instances = nectar.list_instances()
    print(instances)
