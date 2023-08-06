
import setuptools

long_description = \
	"C++ extension with functions for which python is too slow."

setuptools.setup(
	name = "ninty",
	version = "0.0.1",
	description = "Fast functions for Nintendo formats",
	long_description = long_description,
	author = "Yannik Marchand",
	author_email = "ymarchand@me.com",
	url = "https://github.com/kinnay/ninty",
	license = "MIT",
	
	ext_modules = [
		setuptools.Extension("wiiulib.adpcm", ["src/module_adpcm.cpp"]),
		setuptools.Extension("wiiulib.endian", ["src/module_endian.cpp"]),
		setuptools.Extension("wiiulib.gx2", ["src/module_gx2.cpp"]),
		setuptools.Extension("wiiulib.lzss", ["src/module_lzss.cpp"]),
		setuptools.Extension("wiiulib.yaz0", ["src/module_yaz0.cpp"])
	]
)
