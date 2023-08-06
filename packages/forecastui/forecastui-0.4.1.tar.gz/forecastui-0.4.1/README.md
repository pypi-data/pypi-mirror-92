# ForecastUI

An user interface designed to acquire and log data from the Forecast board.

Currently the main user interface of the [Forecast Framework](https://gitlab.com/altairLab/elasticteam/forecastnucleoframework)


## Table of Contents

- [How to install](#how-to-install)
    - [Linux](#linux)
    - [Windows](#windows)
    - [From source](#from-source)

## How to install

### Linux

Refer to the automated installer [script collection](https://gitlab.com/altairLab/elasticteam/forecast/get-forecast)

### Windows
Make sure to have Python installed (version >= 3.5), otherwise download it from [here](https://www.python.org).
```bash
pip install forecastui
```

### From source
Installing from source is not recommended and should be done only by developers and maintainers.

Still here? You are required to have node installed to compile the frontend. As such I suggest [nvm](https://github.com/nvm-sh/nvm) to manage nodejs versions.

Clone the repository
```bash
git clone https://gitlab.com/altairLab/elasticteam/forecast-atlas.git
cd forecast-atlas
```
Compile the frontend
```bash
make build
```
Install the package
```bash
pip install -e .
```

Start the app
```bash
forecastui
```
