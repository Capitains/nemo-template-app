# Installing Python 3 on Mac and Ubuntu

We recommend using Python 3 for this tutorial. Earlier versions can cause problems.

## Installation

### OS X

__We recommmend that you install the Anaconda distribution.__ It has the necessary modules and packages for this tutorial. 
It is available on all platforms and has a simple installation procedure. You can download it from http://continuum.io/downloads. 
Installation instructions can be found at http://docs.continuum.io/anaconda/install.html. 

Install the most recent version of 3.6. Once it is installed, enter the following on your terminal:

```conda create -n cours-python```

Followed by 

```source activate cours-python```

This last step activates a local python environment, preventing changes the general python environment on your computer.

__From within the directory containing your local git clone of this tutorial's repository on your machine__, enter the following commands on the terminal:

```pip install -r requirements.txt```

### Linux (Ubuntu/Debian)

__N.B. you will need administrator rights to follow these instructions.__

Open a terminal window and enter:

```sudo apt-get install python3 libfreetype6-dev python3-pip python3-virtualenv```

Once installed, enter:

```virtualenv ~/.cours-python -p python3```

That will create a virtual environment in which you can install all of the necessary libraries. 

At the terminal, __enter the directory containing the local git clone of this tutorial's repository on your machine__, and from within this directory 
type the following commands:

```source ~/.cours-python/bin/activate```

You will need to type this each time you want to work on the tutorial. 

From within the same terminal and directory now type:

```pip install -r requirements.txt```

This will install the packages necessary for this tutorial. 

## Contributors

* Mike Kestemont

* Folgert Karsdorp

* Maarten van Gompel

* Matt Munson

* Thibault Clérice

* Bridget Almas



