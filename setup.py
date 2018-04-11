from cx_Freeze import Executable, setup
import sys

exeBuildOpts = dict(include_files = ['img/', 'Home/', 'public/'])
sys.argv.append('build')
setup(
	name = 'BitNET',
	version = '0.1',
	author = 'Praneet',
	description = 'PyQt5 Web Browser using Webkit',
	options = dict(build_exe = exeBuildOpts),
	executables = [Executable("smartBrowse.py")],
	)

sys.argv[1] = 'bdist_msi'
setup(
	name = 'BitNET',
	version = '0.1',
	author = 'Praneet',
	description = 'PyQt5 Web Browser using Webkit',
	executables = [Executable("smartBrowse.py")],
	)