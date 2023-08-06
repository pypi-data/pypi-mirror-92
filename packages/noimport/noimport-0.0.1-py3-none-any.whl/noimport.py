import sys

#No importing
sys.path = []
sys.meta_path = []

for key in sys.modules.keys():
	sys.modules[key] = None

sys.builtin_module_names = []
sys.path_hooks = []

for key in sys.path_importer_cache.keys():
	sys.path_importer_cache[key] = None