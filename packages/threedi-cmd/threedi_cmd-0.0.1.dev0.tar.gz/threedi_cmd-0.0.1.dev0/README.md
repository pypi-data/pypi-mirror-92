# The 3Di command line client

The 3Di command line client allows for 

 - Defining and running 3Di scenarios from the command line. 
 - Assembling different scenarios as a "suite" that will be run in batch.    
 - Management commands, for instance to list currently running simulations. 
 
There are three main entry points for the 3Di command line client.

## Scenario command

```
$ scenario --help

Usage: scenario [OPTIONS] COMMAND [ARGS]...

Options:
  --endpoint [localhost|staging|production]
                                  The endpoint where commands are run against
  --help                          Show this message and exit.

Commands:
  auth           Provide authentication details
  models         List available threedimodels
  organisations  List available organisations
  results        Download results of a simulation
  run            Run a given scenario
  scenarios      List local scenarios
  settings       Set default settings
  simulations    List simulations
```


## Suite command

```
$ suite --help

Usage: suite [OPTIONS]

  run suite a given suite

Options:
  --suite PATH  path to the suite file  [required]
  --help        Show this message and exit.
``` 


## Active simulations command

```
$ active_simulations --help

Usage: active_simulations [OPTIONS]

  Show currently running simulations

Options:
  --endpoint [localhost|staging|production]
                                  The endpoint where commands are run against
  --help                          Show this message and exit.

```

## Dependencies

`python >= 3.8`


## Installation

Dependencies python >= 3.8

```
pip install --user 3Di-cmd-client
```


