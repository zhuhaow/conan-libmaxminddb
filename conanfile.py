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

                autotools = AutoToolsBuildEnvironment(self)
                autotools.configure(args=args)
                autotools.make()
                autotools.install()
            else:
                with tools.vcvars(self.settings):
                    sdk = tools.get_env("WindowsSDKVersion").strip(" \\")

                msbuild = MSBuild(self)
                msbuild.build(
                    "projects/VS12/libmaxminddb.sln",
                    properties={"WindowsTargetPlatformVersion": sdk},
                )

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
