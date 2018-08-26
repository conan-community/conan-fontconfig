from conans import ConanFile, CMake, tools, AutoToolsBuildEnvironment


class FontconfigConan(ConanFile):
    name = "fontconfig"
    version = "2.13.0"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Fontconfig here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "pkg_config"

    def requirements(self):
        self.requires("freetype/2.9.0@bincrafters/stable")

    def build_requirements(self):
        self.build_requires("gperf/3.1@jgsogo/stable")

    def source(self):
        url = "https://www.freedesktop.org/software/fontconfig/release/fontconfig-{version}.tar.gz"
        tools.get(url.format(version=self.version))

    def build(self):
        autotools = AutoToolsBuildEnvironment(self)

        prefix = '/home/jgsogo/.conan/data/freetype/2.9.0/bincrafters/stable/package/1e25f8fc336196e0898e984c1f0498b55571827c'
        libdir = prefix + '/lib'
        includedir = prefix + '/include'
        includedir3 = prefix + '/include/freetype2'
        LIBS = '-L{libdir} -lfreetype -lm -Wl,-rpath="{libdir}"'.format(libdir=libdir)
        CFLAGS = '-I${includedir} -I${includedir3}'.format(includedir=includedir, includedir3=includedir3)

        with tools.environment_append({'FREETYPE_LIBS': LIBS, 'FREETYPE_CFLAGS': CFLAGS}):
            autotools.configure(configure_dir="{name}-{version}".format(name=self.name, version=self.version))
            autotools.make()

    def package(self):
        with tools.chdir(self.build_folder):
            self.run("make install")

    def package_info(self):
        self.cpp_info.libs = ["fontconfig",]

