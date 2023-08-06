import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dota2_grid_editor_cli",
    version="1.1.0",
    author="psyche_wolf",
    author_email="jaforjaber@gmail.com",
    description="CLI for dota2_grid_editor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Psychewolf/dota2_grid_editor",
    install_requires=[
   'requests',
   'pandas'
		],
    py_modules       = ["cli_grid"],
    entry_points     = """
            [console_scripts]
            cli_grid = cli_grid:cli_grid
        """,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)