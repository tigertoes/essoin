from setuptools import setup, find_packages, Command


class FuzzCommand(Command):
    description = 'Enables fuzz testing of the parser'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from fuzz import fuzz_runner
        fuzz_runner()


setup(
    name='essoin',
    version='1.0.0',
    packages=find_packages(),
    license='Apache 2',
    test_suite='test',
    tests_require=['pythonfuzz'],
    cmdclass={
        'fuzz': FuzzCommand 
    }
)
