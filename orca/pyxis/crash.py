import subprocess

def convert_mp3_to_wav(input_filename, output_filename):

    if sys.platform.startswith("win"):
        # Don't display the Windows GPF dialog if the invoked program dies.
        # See comp.os.ms-windows.programmer.win32
        # How to suppress crash notification dialog?, Jan 14,2004 -
        # Raymond Chen's response [1]

        import ctypes
        SEM_NOGPFAULTERRORBOX = 0x0002 # From MSDN
        ctypes.windll.kernel32.SetErrorMode(SEM_NOGPFAULTERRORBOX);
        subprocess_flags = 0x8000000 #win32con.CREATE_NO_WINDOW?
    else:
        subprocess_flags = 0



    """
    converts the incoming mp3 file to wave file
    """
    if not os.path.exists(input_filename):
        raise AudioProcessingException, "file %s does not exist" % input_filename

    #exec("lame {$tmpname}_o.mp3 -f {$tmpname}.mp3 && lame --decode {$tmpname}.mp3 {$tmpname}.wav");
    command = ["lame", "--silent", "--decode", input_filename, output_filename]

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess_flags)
    (stdout, stderr) = process.communicate()

    if process.returncode != 0 or not os.path.exists(output_filename):
        raise AudioProcessingException, stdout

    return output_filename
