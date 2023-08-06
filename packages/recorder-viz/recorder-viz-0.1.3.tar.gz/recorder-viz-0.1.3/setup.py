import setuptools

c_reader_module = setuptools.Extension('lib/librreader',
                                        ['lib/reader.c'], include_dirs=['lib'])

'''
import subprocess
from setuptools.command.build_py import build_py
class my_build(build_py):
    def run(self):
        #_build.run(self)
        subprocess.call(['make', 'clean', '-C', 'lib'])
        subprocess.call(['make', '-C', 'lib'])
        print("HHH")
'''

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="recorder-viz",                # Package name, e.g., pip install recorder-viz
    version="0.1.3",
    author="Chen Wang",
    author_email="wangvsa@gmail.com",
    description="Utilities for processing Recorder traces",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wangvsa/recorder-viz",
    packages=['recorder_viz', 'lib'],          # package for import: after installaion, import recorder_viz
    package_data = {'lib': ['*.h']},            # *.h by default will not be copied, we use this to ship it.
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: University of Illinois/NCSA Open Source License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
    ext_modules=[c_reader_module],
    #cmdclass={'build_py': my_build},
)

