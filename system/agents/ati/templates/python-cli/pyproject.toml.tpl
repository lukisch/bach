[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "${project_name}"
version = "0.1.0"
description = "${description}"
readme = "README.md"
requires-python = ">=3.10"
license = {text = "MIT"}
authors = [
    {name = "Lukas", email = ""}
]
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "ruff>=0.1",
]

[project.scripts]
${project_name} = "${project_name}.cli:main"

[tool.setuptools.packages.find]
where = ["src"]

[tool.ruff]
line-length = 100
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
