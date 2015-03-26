# Spike Build

How to build and deploy using a script

## Requirements

Python Fabric
Vagrant
Git

To be able to run the example the first step after getting the source code is to get the Fabric scripts resources from Github:

```
fab git_clone
```

Then you can go to code and get the vagrant machine that will be our build server

```
cd code
fab prepare_machine

```
