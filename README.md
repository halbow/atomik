# Atomik

Atomik provides you a python-friendly way to manage writing new file and folders in an atomic way.

### File
This will ensure either all the data is correctly written to file or none of it
```
with atomik("./result.json") as f:
    print(stream, file=f)
```

### Folder
```
with atomik("./result_folder") as dir:
    with open(Path(dir, "result_1.json") as f:
        print(result_1, file=f)
    with open(Path(dir, "result_2.json") as f:
        print(result_2, file=f)
```

### Safe default

By default, atomik will not overwrite files/non-empty folders but it's configurable. 

# How ?

It uses Linux rename atomic property to handle this