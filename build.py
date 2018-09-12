from conan.packager import ConanMultiPackager
import platform

if __name__ == "__main__":
    if platform.system() == "Windows":
        builder = ConanMultiPackager(default_archs=["Win32", "x64_64"])
    else:
        builder = ConanMultiPackager()

    builder.add_common_builds(shared_option_name="libmaxminddb:shared")
    builder.run()
