# Read out Values from a Viessmann Heat Pump

Use the PyViCare python API to access information stored on your heatpump in the Viessmann cloud. 

You need to copy over `config.ini.sample` to `config.ini` and enter the credentials. 

Install and run: 
```bash
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ python read.py
```

If you want to read more or different parameters, run `python dump.py` and check the resulting files, what is available. 

Note that some parameters are only available in the paid tier of the Viessmann API.

