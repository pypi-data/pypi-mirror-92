
import setuptools

long_description = \
	"C++ extension with functions for which python is too slow."

setuptools.setup(
	name = "ninty",
	version = "0.0.2",
	description = "Fast functions for Nintendo formats",
	long_description = long_description,
	author = "Yannik Marchand",
	author_email = "ymarchand@me.com",
	url = "https://github.com/kinnay/ninty",
	license = "MIT",
	
	ext_modules = [
		setuptools.Extension("ninty.adpcm", ["src/module_adpcm.cpp"]),
		setuptools.Extension("ninty.endian", ["src/module_endian.cpp"]),
		setuptools.Extension("ninty.gx2", ["src/module_gx2.cpp"]),
		setuptools.Extension("ninty.lzss", ["src/module_lzss.cpp"]),
		setuptools.Extension("ninty.yaz0", ["src/module_yaz0.cpp"])
	]
)
