def getFrom(dockerfile, registry):
    with open(dockerfile) as fh:
        for line in fh:
            if line.strip().startswith('FROM'):
                parts = line.strip().split()
                image_name = parts[1]
                image_name = image_name.replace("$registry", registry)
                break
    return image_name

def getImageId(image):
    cmd = 'docker images | grep %s | grep latest' % image
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    if len(output[1]) > 0:
        print(output[1])
        exit(1)
    if len(output[0]) > 0:
        parts = output[0].split()
        return parts[2]
    else:
        print('no image found for %s' % image)
        exit(1)

