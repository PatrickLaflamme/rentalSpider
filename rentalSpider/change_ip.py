import subprocess
import json

def change_ip():
  def awsExec(cmdList):
    
    result = subprocess.check_output(['aws', 'ec2'] + cmdList)
    
    return json.loads(result)
  
  instance_data = awsExec(["describe-addresses", "--query", "Addresses[?NetworkInterfaceId==`eni-0c321f80`]"])[0]
  
  new_address_data = awsExec(["allocate-address"])
  
  associate_new_address_data = awsExec(['associate-address', '--allocation-id', new_address_data['AllocationId'], '--network-interface-id', instance_data['NetworkInterfaceId']])
  
  old_address = awsExec(['describe-addresses', '--query', 'Addresses[?InstanceId!=`' + instance_data['InstanceId'] + "`]"])[0]
  
  release_old_address_data = subprocess.call(['aws','ec2','release-address', '--allocation-id', old_address['AllocationId']])

