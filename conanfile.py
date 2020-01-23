from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os


class GLVNDConan(ConanFile):
    name = "libglvnd"
    description = "Keep it short"
    topics = ("conan", "libname", "logging")
    url = "https://github.com/bincrafters/conan-libname"
    homepage = "https://github.com/original_author/original_lib"
    license = "MIT"  # Indicates license type of the packaged library; please use SPDX Identifiers https://spdx.org/licenses/
    # Remove following lines if the target lib does not use CMake
    exports_sources = ["CMakeLists.txt"]
    version = "None"
    # Options may need to change depending on the packaged library
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    _extractionfolder = "source_subfolder"
    _source_subfolder = "source_subfolder/libglvnd-v1.2.0"
    _build_subfolder = "build_subfolder"

    requires = (
        "zlib/1.2.11",
    )

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        tools.download("https://gitlab.freedesktop.org/glvnd/libglvnd/-/archive/v1.2.0/libglvnd-v1.2.0.zip", "libglvnd.zip")
        tools.unzip("libglvnd.zip", self._extractionfolder)
#         tools.replace_in_file(self._source_subfolder + "/CMakeLists.txt", "project(VTK)",
#                               '''project(VTK)
# include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
# conan_basic_setup()''')

    def build(self):
        os.chdir(self._source_subfolder)
        if self.settings.os == 'Linux':
            self.run("chmod +x autogen.sh")
        self.run("./autogen.sh")
        autotools = AutoToolsBuildEnvironment(self)
        autotools.configure()
        autotools.make()

    def package(self):
        # self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        # cmake = self._configure_cmake()
        # cmake.install()
        # # If the CMakeLists.txt has a proper install method, the steps below may be redundant
        # # If so, you can just remove the lines below
        os.chdir(self._source_subfolder)
        autotools = AutoToolsBuildEnvironment(self)
        autotools.configure()
        autotools.install()
        
        include_folder = os.path.join(self._source_subfolder, "include")
        self.copy(pattern="*", dst="include", src=include_folder)
        self.copy(pattern="*.dll", dst="bin", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
