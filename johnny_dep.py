'''
    This script was made to demonstrate to a friend, Johnathan, how to
    obtain a pip dependency tree for a given package recursively by using
    Python default setup (libraries and pip installation).

    This script requires the package to first be installed via pip. I.e.:
        pip install <package_name>

    2022-04-07

    Usage:
        python johnny_dep.py <package name>
'''

import sys
import subprocess


def get_requirements(package):
    output = subprocess.Popen(
        f'pip show {package}',
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        stdin=subprocess.PIPE,
        shell=True,
        bufsize=0
    ).stdout.read().decode(errors='ignore')
    
    output_lines = output.split('\n')
    
    for line in output_lines:
        if 'Requires: ' in line:
            return line.strip('Requires:').split(', ')

def johnny_dep(package):
    if not package:
        return

    print(package)
    for requirement in get_requirements(package):
        johnny_dep(requirement.strip().rstrip())


'''
    This function call was purposely left out of the Python __main__ block
    for deliterate recursive confusion when importing this file. Ideally
    it should be called in a block like this:

    if __name__=='__main__':
        package = sys.argv[1]
        johnny_dep(package)
'''
package = sys.argv[1]
johnny_dep(package)
