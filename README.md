# Read out Values from a Viessmann Heat Pump

Use the PyViCare python API to access information stored on your heatpump in the Viessmann cloud. 

You need to copy over `config.ini.sample` to `config.ini` and enter the credentials. 
In order to use this, you need to register a Viessmann ViCare account, and register a client ID at http://developer.viessmann.com (Login with you ViCare account).

Install and run: 
```bash
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ python read.py
```

If you want to read more or different parameters, run `python dump.py` and check the resulting dumps, to see what is available. 

Note that some parameters are only available in the paid tier of the Viessmann API.

I added a visualization of the data, see [here](heatpump_visuals.ipynb).

This is based on the [PyViCare](https://github.com/openviess/PyViCare) library.
