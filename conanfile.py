from conans import ConanFile, tools, AutoToolsBuildEnvironment, MSBuild


class LibmaxminddbConan(ConanFile):
    name = "libmaxminddb"
    version = "1.3.2"
    license = "Apache License, Version 2.0"
    url = "https://github.com/maxmind/libmaxminddb"
    description = "C library for the MaxMind DB file format"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = ("shared=False", "fPIC=True")

    def configure(self):
        del self.settings.compiler.libcxx
        if self.settings.compiler == 'Visual Studio':
            del self.options.fPIC

    def source(self):
        self.run("git clone --recursive https://github.com/maxmind/libmaxminddb")
        self.run("cd libmaxminddb && git checkout 1.3.2")

    def build(self):
        with tools.chdir("libmaxminddb"):
            if self.settings.compiler != "Visual Studio":
                self.run("autoreconf -fiv", run_environment=True)

                args = ["--prefix=%s" % self.package_folder]
                if self.options.shared:
                    args.extend(["--disable-static", "--enable-shared"])
                else:
                    args.extend(["--disable-shared", "--enable-static"])
                if self.settings.build_type == "Debug":
                    args.append("--enable-debug")
                if self.options.fPIC:
                    args.append("--with-pic")
                else:
                    args.append("--without-pic")
                if not tools.get_env("CONAN_RUN_TESTS", True):
                    args.append("--disable-tests")

                autotools = AutoToolsBuildEnvironment(self)
                autotools.configure(args=args)
                autotools.make()
                if tools.get_env("CONAN_RUN_TESTS", True):
                    self.run("make check")
                autotools.install()
            else:
                if self.options["shared"]:
                    self.output.warning(
                        "libmaxminddb does not support building dynamic library yet, building static library instead"
                    )
                    self.options["shared"] = False

                with tools.vcvars(self.settings):
                    sdk = tools.get_env("WindowsSDKVersion")
                    if sdk:
                        sdk = sdk.strip(" \\")

                msbuild = MSBuild(self)
                msbuild.build(
                    "projects/VS12/libmaxminddb.sln",
                    targets=["libmaxminddb"],
                    properties={"WindowsTargetPlatformVersion": sdk} if sdk else {},
                    platforms={"x86": "Win32"},
                )

    def package(self):
        self.copy("*.h", src="libmaxminddb/include", dst="include")
        self.copy("*libmaxminddb*.lib", dst="lib", keep_path=False)
        self.copy("*libmaxminddb*.dll", dst="bin", keep_path=False)
        self.copy("*libmaxminddb.so", dst="lib", keep_path=False)
        self.copy("*libmaxminddb.dylib", dst="lib", keep_path=False)
        self.copy("*libmaxminddb.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
