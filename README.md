# crafterlib

Copyright (C) 2025 Jacob Farnsworth

Have you ever played a game with some kind of crafting system? Have you ever found yourself struggling to plan your crafting goals in such a game? Maybe you've wondered, "How much stone do I need to make 1000 slabs?" or "How many sticks and ingots do I need to make 4 pickaxes?"

crafterlib is a Python library that can help with a variety of crafting and resource management-related math. crafterlib can help with all kinds of queries related to crafting in your favorite games, and more!

crafterlib is maintained by faculty and students of Gymnasieingenjörsprogrammet-TE4 at NTI Gymnasiet Karlstad as an educational resource in professional-grade software development.

## Features

crafterlib is currently in alpha, so features may be buggy or unavailable.

* Built-in item and crafting data for several popular games (Minecraft, Stardew Valley). Make queries related to items, recipes, and crafting.
* Advanced crafting math: Determine the number of a certain ingredient needed to craft a certain item, or the number of items that you can produce with a given set of ingredients.
* Resource types: Is an item a basic resource (can't be crafted), an intermediate resource (crafting ingredient and product) or an advanced resource (only a crafting product)?

## Upcoming Features

* Comprehensive crafting plans: Given a desired item, crafterlib will give you a step-by-step crafting to-do list. Say you want to craft 2 Iron Blocks, crafterlib will give you a step-by-step to-do list such as:
  - "Gather 3 Coal. (Mining)"
  - "Gather 18 Raw Iron. (Mining)"
  - "Craft 18 Iron Ingots. (Smelting)"
  - "Craft 2 Iron Blocks. (Crafting)"
  - ... and after you're done, you'll have 1 leftover Coal.

## Installing

### Quick Start With pip

If you just want to build something using crafterlib, you can follow these instructions.

crafterlib is tested on Python versions 3.10 and later. Ensure you have Python 3.10 or later installed before proceeding.

You can install the latest version of crafterlib with the following command:

```
pip install git+https://github.com/JFarNTIG/crafterlib.git@v0.1.0
```

After this, it's quick and easy to import crafterlib in your project and get started:

```python
import crafterlib
import crafterlib.craftutils as craftutils
```

If you'd like to see some example programs that use crafterlib, check out the `examples/` directory.


### For Developers

If you'd like to use the latest features of crafterlib or work on crafterlib itself, here are the recommended instructions for installing crafterlib from source.

#### Create Environment

Start by cloning the crafterlib repository into a new directory:

```
git clone https://github.com/JFarNTIG/crafterlib && cd crafterlib
```

It's recommended to create a Python virtual environment (venv) before installing crafterlib:
```
python -m venv .venv
```

Next, activate the venv. Refer to the instructions for your platform.

**Terminal (Linux)**
```
source .venv/bin/activate
```

**Terminal (Windows)**
```
.venv\Scripts\activate
```

**Visual Studio Code (All Platforms)**

To activate the venv in VS Code, open the menu to select Python runtime (bottom right-hand corner). Choose the venv.

If you plan on working on crafterlib itself, it's recommended to create a Python virtual environment (venv) before you install crafterlib. You can use the following command:
```
python -m venv .venv
```

#### Install crafterlib

After cloning the repository and making your venv, you can install the crafterlib package locally in editable mode with test dependencies:

```
pip install -e .[test]
```

#### Unit Tests

Unit tests are located in the `tests/` folder.

Run all unit tests:
```
pytest
```

Run all unit tests and get a detailed coverage report, including missed lines:
```
pytest --cov-report term-missing
```

## Contributing

You'd like to contribute to crafterlib? Great!

* `docs/style.md` for code style guide.

Remember to use the PR template when submitting a PR.

## License

crafterlib is licensed under the terms of the MIT License. See the file `LICENSE` for the full license text.