from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain
from conan.tools.files import rmdir
import os


required_conan_version = ">=2.0"


class DirectXHeadersConan(ConanFile):
    name = "directx-headers"
    version = "1.613.0"
    python_requires = "aleya-conan-base/1.3.0@aleya/public"
    python_requires_extend = "aleya-conan-base.AleyaConanBase"

    exports_sources = "source/*"

    options = {
        "shared": [False, True],
        "fPIC": [False, True]
    }

    default_options = {
        "shared": False,
        "fPIC": True
    }

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["BUILD_SHARED_LIBS"] = self.options.shared
        tc.variables["BUILD_TESTING"] = False
        tc.generate()
        tc = CMakeDeps(self)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

        rmdir(self, os.path.join(self.package_folder, "share"))
        rmdir(self, os.path.join(self.package_folder, "lib", "pkgconfig"))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "directx-headers")

        self.cpp_info.components["directx-headers"].libs = ["DirectX-Headers"]
        self.cpp_info.components["directx-headers"].set_property("cmake_target_name", "Microsoft::DirectX-Headers")

        if self.settings.os == "Windows":
            self.cpp_info.components["directx-headers"].includedirs = ["include"]
        else:
            self.cpp_info.components["directx-headers"].includedirs = ["include", "include/wsl/stubs"]

        self.cpp_info.components["directx-guids"].libs = ["DirectX-Guids"]
        self.cpp_info.components["directx-guids"].set_property("cmake_target_name", "Microsoft::DirectX-Guids")
