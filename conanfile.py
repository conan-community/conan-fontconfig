
import os
import shutil

from conans import ConanFile, CMake, tools, AutoToolsBuildEnvironment


class FontconfigConan(ConanFile):
    name = "fontconfig"
    version = "2.13.1"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Fontconfig here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "pkg_config"

    def requirements(self):
        self.requires("freetype/2.9.0@bincrafters/stable")
        if self.settings.os == "Linux":
            self.requires("libuuid/1.0.3@bincrafters/stable")

    def build_requirements(self):
        self.build_requires("gperf/3.1@jgsogo/stable")

    def source(self):
        url = "https://www.freedesktop.org/software/fontconfig/release/fontconfig-{version}.tar.gz"
        tools.get(url.format(version=self.version))

        # Patch files from project itself
        #  - fontconfig requires libtool version number, change it for the corresponding freetype one
        tools.replace_in_file(
            os.path.join(self.source_folder, '{}-{}'.format(self.name, self.version), 'configure'),
            '21.0.15', '2.8.1')

    def _patch_pc_files(self):
        # Patch freetype2
        freetype_path = self.deps_cpp_info["freetype"].rootpath
        shutil.copyfile(os.path.join(freetype_path, "lib", "pkgconfig", "freetype2.pc"),
                        "freetype2.pc")
        tools.replace_prefix_in_pc_file("freetype2.pc", freetype_path)

    def build(self):
        # Patch files from dependencies
        self._patch_pc_files()

        autotools = AutoToolsBuildEnvironment(self)
        autotools.configure(
            configure_dir="{name}-{version}".format(name=self.name, version=self.version))
        autotools.make()

    def package(self):
        with tools.chdir(self.build_folder):
            self.run("make install")

    def package_info(self):
        self.cpp_info.libs = ["fontconfig", ]

