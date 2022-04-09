'''
    This script was made to demonstrate to a friend, Johnathan, how to
    obtain a pip dependency tree for a given package recursively by using
    Python default setup (libraries and pip installation).

    This script requires the package to first be installed via pip. I.e.:
        pip install <package_name>
        pip install pandas

    2022-04-07

    Usage:
        python johnny_dep.py <package name>
        python johnny_dep.py pandas
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
            return line.strip('Requires:').rstrip().replace(' ', '').split(',')
    return []

def johnny_dep(package):
    if not package:
        return

    print(package)
    for requirement in get_requirements(package):
        johnny_dep(requirement)

def johnny_seq(package):
    packages = [package]
    while packages != []:
        next_package = packages.pop(0)
        if not next_package:
            continue
        print(next_package)
        packages += get_requirements(next_package)

def pip_dep(package, dependencies):
    if not package:
        return
    
    dependencies[package] = get_requirements(package)
    for requirement in dependencies[package]:
        if requirement in dependencies:
            continue
        pip_dep(requirement, dependencies)

def pip_seq(package, dependencies={}):
    packages = [package]
    while packages != []:
        next_package = packages.pop(0)
        if not next_package or next_package in dependencies:
            continue
        dependencies[next_package] = get_requirements(next_package)
        packages += dependencies[next_package]
    return dependencies

'''
    This function call was purposely left out of the Python __main__ block
    for deliberate recursive confusion when importing this file. Ideally
    it should be called in a block like this:

    if __name__=='__main__':
        package = sys.argv[1]
        johnny_dep(package)
'''
package = sys.argv[1]

print('\nCalling recursively:')
johnny_dep(package)

print('\nCalling sequentially:')
johnny_seq(package)

print('\nCalling recursively while displaying properly:')
dependencies = {}
pip_dep(package, dependencies)
for dependency in dependencies:
    print(dependency)
    for requirement in dependencies[dependency]:
        if requirement:
            print(f'\t{requirement}')

print('\nCalling sequentially while displaying properly:')
dependencies = pip_seq(package)
for dependency in dependencies:
    print(dependency)
    for requirement in dependencies[dependency]:
        if requirement:
            print(f'\t{requirement}')
