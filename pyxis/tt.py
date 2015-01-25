import subprocess
cmd=['/bin/sleep', '60']
job_folder='/home/madlee'
subprocess_flags=0
process = subprocess.Popen(cmd, cwd=job_folder, creationflags=subprocess_flags)
print process.wait()
