from conans import ConanFile, CMake
import os

channel = os.getenv("CONAN_CHANNEL", "testing")
username = os.getenv("CONAN_USERNAME", "robertobernabe")


class SnappyTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "libressl/3.0.0@%s/%s" % (username, channel)
    # default_options = "libressl:system=True", "libressl:root=/tmp/sss", "libressl:shared=true"
    default_options = "libressl:shared=True"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        self.run('cmake "%s" %s' % (self.source_folder, cmake.command_line))
        self.run("cmake --build . %s" % cmake.build_config)

    def imports(self):
        self.copy(pattern="*.dll", dst="bin", src="bin")
        self.copy(pattern="*.dylib*", dst="bin", src="lib")
        self.copy(pattern="*.so*", dst="lib", src="lib")

    def test(self):
        os.chdir("bin")
        self.run(".%stest" % os.sep)
