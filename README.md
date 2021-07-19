# About TimeTracker 5280 <a
> The TimeTracker 5280 is a CLI that allows users to track the amount of time they have spent working on different tasks throughout the day. Though there are other solutions for time tracking, this provides a quick (and dirty) local interface that requires minimal interaction and thereby increases efficiency.

## Table of Contents
* [About](#about-timetracker-5280)
* [Setup](#setup)
* [Usage](#usage)


## Setup
### Install File(s)
There really is only one file that needs to be installed to run this system (time-tracker.py). However, I recommend you download the README to use as reference. Additionally, I recommend downloading the files to their own, dedicated folder so as to minimize the chance of messing up the alias (created in the next step).

### Install requirements
Make sure you install the following libraries:
* argparse==1.4.0
* datetime==4.3
* pathlib==1.0.1
* pandas==1.1.3
OR<br>
You can run `pip install -r requirements.txt`)



### Create a Command Line Alias
#### MAC (zsh)
1. Open your .zshrc file (typically located at \~/.zshrc)
2. Add the following line of code to the bottom of the file:
`alias tt="python [absolute path of your time-tracker.py file]`
3. Restart terminal and ensure the system runs by entering:
`tt start -t 12:30 -n 'test'`

#### PC
*TBD*

## Usage
Every command should follow a similar format and will call the script (the alias `tt` created above) first, followed by a master command, then followed by optional arguments. For example, the command `tt start -d '2021-07-19' -t '12:30'` will start a task on July 19th, 2021 at 12:30pm. The following will explain the functionality of each master command and its accompanying arguments.

### start (`start`, `open`)
*Open a task record*
| Argument | Symbols    | Examples                                              | Usage                                                        | Notes                                                          |
|----------|------------|-------------------------------------------------------|--------------------------------------------------------------|----------------------------------------------------------------|
| name     | -n, --name | -n task <br> --name 'test task' <br> -n 'test task'   | Assigns a name to the task being started                     | Single word doesn't need quotes<br> Multiple words need quotes |
| date     | -d, --date | -d 20210708 <br> --date 2021-02-04 <br> -d 2020-08-26 | Manually sets the date of the task (default is current date) | Accepted date formats:<br> '%Y-%m-%d', '%Y%m%d'                |
| time     | -t, --time | -t 12:45<br> --time 13:30                             | Manually sets the time of the task (default is current time) | Time is in a 24 hour format, <br> with or without ':'          |

### stop (`stop`, `close`, `end`)
*Close a task and record the elapsed time of working on the task*
| Argument | Symbols     | Examples                                              | Usage                                                              | Notes                                                          |
|----------|-------------|-------------------------------------------------------|--------------------------------------------------------------------|----------------------------------------------------------------|
| name     | -n, --name  | -n task <br> --name 'test task' <br> -n 'test task'   | Specifies the name of the task you wish to end                     | Single word doesn't need quotes<br> Multiple words need quotes |
| index    | -i, --index | -i 0 <br> --index                                     | Specifies the index of the task you wish to end                    | Index must be within in range (can check index with `show`)    |
| date     | -d, --date  | -d 20210708 <br> --date 2021-02-04 <br> -d 2020-08-26 | Manually sets the date to close the task (default is current date) | Accepted date formats:<br> '%Y-%m-%d', '%Y%m%d'                |
| time     | -t, --time  | -t 12:45<br> --time 13:30                             | Manually sets the time to close the task (default is current time) | Time is in a 24 hour format, <br> with or without ':'          |

### edit (`edit`, `adjust`, `change`)
*Edit the details of a previously created task*
| Argument | Symbols     | Examples                                              | Usage                                            | Notes                                                          |
|----------|-------------|-------------------------------------------------------|--------------------------------------------------|----------------------------------------------------------------|
| name     | -n, --name  | -n task <br> --name 'test task' <br> -n 'test task'   | Specifies the name of the task you wish to edit  | Single word doesn't need quotes<br> Multiple words need quotes |
| index    | -i, --index | -i 0 <br> --index                                     | Specifies the index of the task you wish to edit | Index must be within in range (can check index with `show`)    |

### clear (`clear`)
*Delete all tasks permanently*

### show (`show`)
*Show all current tasks and their details*

### delete (`delete`)
*Delete a previously created task permanently*
| Argument | Symbols     | Examples                                              | Usage                                              | Notes                                                          |
|----------|-------------|-------------------------------------------------------|----------------------------------------------------|----------------------------------------------------------------|
| name     | -n, --name  | -n task <br> --name 'test task' <br> -n 'test task'   | Specifies the name of the task you wish to delete  | Single word doesn't need quotes<br> Multiple words need quotes |
| index    | -i, --index | -i 0 <br> --index                                     | Specifies the index of the task you wish to delete | Index must be within in range (can check index with `show`)    |

### sum (`sum`)
*Show to total number of hours worked on all tasks*



