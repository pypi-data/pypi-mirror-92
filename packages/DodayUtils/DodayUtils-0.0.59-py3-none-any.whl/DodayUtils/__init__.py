import os
from importlib import import_module

my_location = os.path.dirname(__file__)
module_list = [file
			   for file in os.listdir(my_location)
			   if os.path.splitext(file)[1] == '.py'
			   and file != '__init__.py']

modules = [import_module(f'.{os.path.splitext(module)[0]}', __name__)
		   for module in module_list]

globals().update({name: getattr(module, name)
                  for module in modules
                  for name in module.__dict__
                  if not name.startswith('_')})