# -*- coding: utf-8 -*-
import os
import importlib

class UnknownEndpoint(Exception):
    pass

class PluginCollection:
    _modules = {}

    def __init__(self, plugin_source, alt_pkg=None):
        self.plugin_source = plugin_source
        self.alt_pkg = alt_pkg

    def load(self, name="dummy", options={}, dry_run=False, **kwargs):
        if (name in self._modules):
            print("Module already loaded: {0}.{1}".format(self.plugin_source, name))
            return True

        try:
            print("Loading local module {0}.{1}".format(self.plugin_source, name))
            endpoint_module = importlib.import_module("{0}.{1}".format(self.plugin_source, name))
            endpoint_module.register(name, self)
            print("Driver registered: {0}.{1}".format(self.plugin_source, name))
            return True
        except Exception as e:
            print(e)
            if (self.alt_pkg == None):
                print("Invalid drive: {0}.{1}".format(self.plugin_source, name))
                return False
            else:
                try:
                    print("Loading pip module {0}{1}".format(self.alt_pkg, name))
                    endpoint_module = importlib.import_module("{0}{1}".format(self.alt_pkg, name))
                    endpoint_module.register(name, self)
                    print("Driver registered: {0}{1}".format(self.self.alt_pkg, name))
                    return True
                except Exception as e:
                    print(e)
                    print("Invalid drive: {0}{1}".format(self.alt_pkg, name))
                    return False

    def plugin_exist(self, module_name):
        if (module_name in self._modules):
            return True
        else:
            return False

    def add_class(self, module_name, endpoint_class):
        if (module_name not in self._modules):
            self._modules[module_name] = {}
        self._modules[module_name][endpoint_class.name] = endpoint_class

    def get_instance(self, module_name, class_name, **options):
        if (module_name in self._modules):
            if (class_name in self._modules[module_name]):
                print("Class exists: {0}.{1}".format(module_name, class_name))
                endpoint_class = self._modules[module_name].get(class_name)
                return endpoint_class(payload=options)
            else:
                raise ValueError("Invalid Class name: {0}.{1}".format(module_name, class_name))
        else:
            raise ValueError("Invalid module name: {0}".format(module_name))


