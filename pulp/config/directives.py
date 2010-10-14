# encoding: utf-8

__all__ = ['include']


def include(declaration):
    """ Include another YAML file """
    expect_names = ['package', 'filename', 'override']
    declaration.expect(dict, names=expect_names)
    package = declaration.string('package')
    if package is not None:
        package = declaration.resolve(package)
    else:
        package = declaration.context.current_package()
    filename = declaration.string('filename', 'configure.yml')
    override = declaration.string('override',
                                  declaration.context.current_override())
    declaration.context.load(filename, package, override)
