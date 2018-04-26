from nectar import ec2_conn

images = ec2_conn.get_all_images()

for img in images:
    print('Image Id: {}, image name: {}'.format(img.id, img.name))
