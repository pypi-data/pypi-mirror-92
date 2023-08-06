#/bin/python

def get_public_ip():
    from urllib.request import urlopen
    import re
    data = str(urlopen('http://checkip.dyndns.com/').read())
    # data = '<html><head><title>Current IP Check</title></head><body>Current IP Address: 65.96.168.198</body></html>\r\n'
    return re.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(data).group(1)

def get_sg(sg_name: str, profile: str):
    import boto3
    sg_name = sg_name or 'default'
    profile = profile or 'default'

    ec2 = boto3.session.Session(profile_name=profile, region_name='eu-west-1').client('ec2')
    resp = ec2.describe_security_groups()
    target_sg_str = list(filter(lambda x: x['GroupName']==sg_name, resp['SecurityGroups']))
    return target_sg_str

def check_if_aux(ip_permissions: list):
    try:
        return 'Aux' in ip_permissions['IpRanges'][0]['Description']
    except IndexError as e:
        assert ip_permissions['IpRanges']==[]
        return False

def update_sg_to_ip(sg_name='jakub', # ip='2.222.105.71/32',
                    ports=[22, 8501, 8888], profile='default'):
    import boto3

    ip = f"{get_public_ip()}/32"

    ec2 = boto3.session.Session(profile_name=profile, region_name='eu-west-1').client('ec2')
    profile = profile or 'default'

    target_sg_str = get_sg(sg_name, profile=profile)[0]
    ec2_res = boto3.session.Session(profile_name=profile, region_name='eu-west-1').resource('ec2')
    sg_res = ec2_res.SecurityGroup(target_sg_str['GroupId'])

    # loop using description to only remove Aux and not e.g. NFS or Home
    # old port-based solution
    # permissions_to_revoke = [ s for s in sg_res.ip_permissions if s['FromPort'] in ports ]
    permissions_to_revoke = [ s for s in sg_res.ip_permissions if check_if_aux(s) ]

    # Removes all relevant permissions from this group (originally as `jakub`)
    if sg_res.ip_permissions!=[]:
        sg_res.revoke_ingress(IpPermissions=permissions_to_revoke)


    description = 'Jakub Aux Jupyter'
    description2 = 'Jakub Aux SSH'
    description3 = 'Jakub Aux Streamlit'
    data = ec2.authorize_security_group_ingress(
            GroupId=target_sg_str['GroupId'],
            IpPermissions=[
                {'IpProtocol': 'tcp',
                'FromPort': 8888,
                'ToPort': 8888,
                'IpRanges': [{'CidrIp': ip, 'Description': description}] },
                {'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{'CidrIp': ip, 'Description': description2}]},
                {'IpProtocol': 'tcp',
                'FromPort': 8501,
                'ToPort': 8501,
                'IpRanges': [{'CidrIp': ip, 'Description': description2}]}
            ])
    print('Ingress Successfully Set %s' % data)
