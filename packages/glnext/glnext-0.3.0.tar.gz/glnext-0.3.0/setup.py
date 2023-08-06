import os
import platform
from setuptools import Extension, setup

PLATFORMS = {'windows', 'linux', 'darwin'}

target = platform.system().lower()

for known in PLATFORMS:
    if target.startswith(known):
        target = known
        break

define_macros = [('BUILD_' + target.upper(), None)]
extra_compile_args = []
extra_link_args = []
include_dirs = []
library_dirs = []
libraries = []

if target == 'windows':
    # extra_compile_args.append('/Z7')
    # extra_link_args.append('/DEBUG:FULL')
    include_dirs.append(os.path.join(os.getenv('VULKAN_SDK'), 'Include'))
    library_dirs.append(os.path.join(os.getenv('VULKAN_SDK'), 'Lib'))
    libraries.append('vulkan-1')

if target == 'linux':
    extra_compile_args.append('-fpermissive')
    libraries.append('vulkan')

glnext = Extension(
    name='glnext',
    sources=['./glnext/glnext.cpp'],
    depends=[
        './glnext/glnext.hpp',
        './glnext/buffer.cpp',
        './glnext/compute_set.cpp',
        './glnext/encoder.cpp',
        './glnext/image.cpp',
        './glnext/instance.cpp',
        './glnext/memory.cpp',
        './glnext/pipeline.cpp',
        './glnext/render_set.cpp',
        './glnext/sampler.cpp',
        './glnext/staging_buffer.cpp',
        './glnext/surface.cpp',
        './glnext/tools.cpp',
        './glnext/transform.cpp',
        './glnext/utils.cpp',
    ],
    define_macros=define_macros,
    extra_compile_args=extra_compile_args,
    extra_link_args=extra_link_args,
    include_dirs=include_dirs,
    library_dirs=library_dirs,
    libraries=libraries,
)

with open('README.md') as readme:
    long_description = readme.read()

setup(
    name='glnext',
    version='0.3.0',
    ext_modules=[glnext],
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cprogrammer1994/glnext',
    author='Szabolcs Dombi',
    author_email='cprogrammer1994@gmail.com',
    license='MIT',
)
