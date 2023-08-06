# hookpy

[![Build Status](https://github.com/FindDefinition/hookpy/workflows/build/badge.svg)](https://github.com/FindDefinition/hookpy/actions?query=workflow%3Abuild)
[![codecov](https://codecov.io/gh/FindDefinition/hookpy/branch/master/graph/badge.svg?token=IO2ONI3AAL)](https://codecov.io/gh/FindDefinition/hookpy)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FFindDefinition%2Fhookpy.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2FFindDefinition%2Fhookpy?ref=badge_shield)

run python with custom hooks.

## Usage

1. create a ```hook-config.json```, add your hooks and observed folders, then save it to your project folder.

2. run python script with ```hookpy /path/to/script.py --option1 --option2=value2```

## TODO

* Add pre-compile mode: load file, compile to ast, modify ast and compile to module.

## License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FFindDefinition%2Fhookpy.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2FFindDefinition%2Fhookpy?ref=badge_large)