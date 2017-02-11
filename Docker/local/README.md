## Workflow

For Makefile images, you can build an image by specifying the component and tag 
on the commandline. 

To make a dev version:
```
$ make VERSION=0.1.0 EXTRAVERSION=-dev build tag
```

To publish a version:
```
$ make VERSION=0.1.0 build tag push
```

