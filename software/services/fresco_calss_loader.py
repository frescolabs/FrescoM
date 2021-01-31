

class FrescoClassLoader:


    def import_class(self, path: str):
        dot_components = path.split('.')
        components = dot_components[1].split('/')
        module_string = '.'.join(components)[1:]
        class_string_components = components[-1].split('_')
        class_string = ''.join([x.capitalize() for x in class_string_components])
        print('Module name ' + module_string)
        print('Class name ' + class_string)
        mod = __import__(module_string, fromlist=[class_string])
        klass = getattr(mod, class_string)
        return klass
