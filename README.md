# Spike Build

How to build and deploy using a script.

Note: I would prefer to use a build and deployment server, but this will do the trick to run a build from the command line.

## Requirements

* Python Fabric
* Vagrant
* Git

To be able to run the example the first step after getting the source code is to get the Fabric scripts resources from Github:
```
fab git_clone
```

Then you can go to code and get the vagrant machine that will be our build server
```
cd code
fab prepare_machine

```

Now you need the source code in the new vagrant instance:
```
fab at_vagrant get_source_code
```

The build itself will be:
```
fab at_vagrant build
```

Now grab the build from the build machine and pass it to production
```
fab at_vagrant get_build deploy configure
```

All in one line:
```
fab at_vagrant cleanup get_source_code build get_build deploy configure start
```

## Notes

There is an interesting article at [hashbangcode](http://www.hashbangcode.com/blog/connecting-vagrant-box-without-vagrant-ssh-command)