# 🦇 raw

A CLI Tool for Tracking Study and Work Time 👾

Still under development... 🛠️

## Installation

### Homebrew

To install ``raw`` via ``Homebrew``, run the following commands in your terminal:
~~~
brew tap dvodnenko/raw

brew install raw
~~~

Install Homebrew [here](https://brew.sh) if you do not have it yet, or run these commands in the terminal:

~~~
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile

eval "$(/opt/homebrew/bin/brew shellenv)"
~~~

## How to Use

❗️ below, if the parameter is in regular brackets - it is required (strict); 
while if it is in square ones - it is an optional parameter (non-strict)

make an association with math

### Tags

Execute ...

* ```raw tags``` to see al of your tags
* ```raw tags --new (tag name)``` to create a new tag...
* ... or ```raw tags --new (comma-separated tags titles)``` to create many tags at one moment

### Sessions

* ```raw begin -t [comma-separated tags titles] -m "[message]" ``` to begin a new session
* ```raw stop``` to finish the session
* ```raw sessions``` - shows all of the finished sessions **on the provided date range...**

### How to Provide the Date Range ?

there are two options for the ```raw sessions``` command:
* --dr
* --lxd
you **must** provide on of them (but not both!)

#### --dr Option

```--dr``` means "dates range". you must provide regular dates range in this pattern:
~~~
(start year)-(start month)-(start day)..(end year)-(end month)-(end day)
~~~
end information is **not** required. if you do not provide it (just "(start).." ) - ``raw`` will automatically set today as the end date.

you can also provide such values as `today` & `all` to the `--dr` option, where `today` means "all the sessions that were started today
AND are finished"

#### --lxd Option

```--lxd``` option just means "last X days". so if you execute ```raw sessions --lxd 7``` 
it will output all the sessions for last 7 days (because "last 7 days"). also, lxd option should be grater 
than zero (because you cannot see information about "last 0 days"). ```--lxd 1``` means "today" (same as ```--dr today```)
