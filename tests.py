from xmlrpclib import ServerProxy

client = ServerProxy("http://localhost:12547", allow_none=True)

users = [['madlee', 'dhl419'], ['dhl419', '1234567']]
id = client.update_users("oicn892#_kSE", users)

print client.query_jobs("oicn892#_kSE", [14])

# print id

# job_id = client.run_shell('madlee', 'dhl419', r'crash.exe', r'.', None)





# Create your tests here.
