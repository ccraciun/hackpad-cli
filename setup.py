from setuptools import setup, find_packages


setup(
        name="hackpad-cli",
        version="0.1",
        author="cosmic",
        author_email="",
        description="",
        url="",
        packages=find_packages(exclude=["tests"]),
        scripts=["hackpad-cli/hpad.py"],
        test_suite="nose.collector",
        install_requires=[
            "docopt",
            "ipython",
            "oauthlib",
            "requests-oauthlib",
            ]
        )
