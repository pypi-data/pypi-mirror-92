# ForecastUI

An user interface designed to acquire and log data from a nucleo board.

Currently the main user interface of the [Forecast Framework](https://gitlab.com/altairLab/elasticteam/forecastnucleoframework)


## Table of Contents

- [How to install](#how-to-install)
    - [Automated installer](#automated-installer)
    - [Pip](#pip)
    - [From source](#from-source)

## How to install

### Automated installer

Refer to the automated installer [script collection](https://gitlab.com/altairLab/elasticteam/forecast/get-forecast)

### Pip

Warning: libraries or other non-python dependencies are not fetched this way, refer to the automated installer mentioned above.

```bash
pip install forecastui
# or
pip install forecastui[qt]
```

### From source
Installing from source is not recommended and should be done only by developers and maintainers.

Still here? You are required to have npm installed to compile the frontend. As such I suggest [nvm](https://github.com/nvm-sh/nvm) to manage nodejs versions.

Clone the repository
```bash
git clone https://gitlab.com/altairLab/elasticteam/forecast-atlas.git
cd forecast-atlas
```
Compile the frontend
```bash
make build
```
Test and start the app
```bash
make run
```
