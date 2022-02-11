## Chiz
Tools to watch a bigbluebutton meeting from moodle and provide an API to easily do certain actions on certain conditions (e.g. join a meeting automatically when it's started.).


Note: This project is made for educational purposes only. Using it for other purposes is outside of the scope of author's responsibilities.


#### Initial setup
First, install the dependencies: 

`python3 -m pip install -r requirements.txt`

Rename `config.py.sample` to `config.py` and open it with a text editor. Change `username`, `password`, and the other parameters to match your needs.

#### Usage
Run any of the `action_*.py` files and use them. Individual documentation is provided as docstrings in each file.

#### Contributing
The `Watchdog` class provides an easy-to-use interface for interacting with courses. Any proposed new actions should only use instances of `Watchdog`, and therefore only need to provide a check function and a callback. Define utility functions in `utils.py` so they can be used by others as well. As an example, see `action_beep.py`.
