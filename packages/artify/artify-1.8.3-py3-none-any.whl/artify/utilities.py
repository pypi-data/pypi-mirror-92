import __main__
from artify import change_version

def get_current_application_version(path):
    if __main__.os.path.exists(__main__.os.path.join(path,'build.gradle')):
        __main__.arch_type = 'gradle'
        filepath = __main__.os.path.join(path,'build.gradle')
        return change_version.get_version(filepath)
        
    if __main__.os.path.exists(__main__.os.path.join(path, 'app', 'build.gradle')):
        __main__.arch_type = 'gradle'
        filepath = __main__.os.path.join(path, 'app', 'build.gradle')
        return change_version.get_version(filepath)
        
    if __main__.os.path.exists(__main__.os.path.join(path,'package.json')):
        __main__.arch_type = 'npm'
        filepath = __main__.os.path.join(__main__.path, 'package.json')
        return change_version.get_version(filepath)

    if __main__.os.path.exists(__main__.os.path.join(path,'pom.xml')):
        __main__.arch_type = 'maven'
        filepath = __main__.os.path.join(path,'pom.xml')
        return change_version.get_version(filepath)

    if __main__.os.path.exists(__main__.os.path.join(path,'pubspec.yaml')):
        __main__.arch_type = 'flutter'
        filepath = __main__.os.path.join(path,'pubspec.yaml')
        return change_version.get_version(filepath)
        
    # To-do Extract version number for .NET type project
    return None