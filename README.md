# 🚀 Atomik 

Atomik provides you a python-friendly way to manage writing new file and folders in an atomic way.
The main way to use the library is with to use the `file` and `folder` context manager. They will provide
an easy interface to make sure **the destination file/folder** remain consistent.

This means you can be sure that you will not leave a file half written or 
a folder with half the files you wanted to write into in case of failure. 
When overwriting you can be sure that the data will be either the previous or the next version.


## 📚 Example
### File
This will ensure either all the data is correctly written to file or none of it
```
with atomik.file("./result.json") as f:
    print(stream, file=f)
```

### Folder
```
with atomik.folder("./result_folder") as dir:
    with open(Path(dir, "result_1.json") as f:
        print(result_1, file=f)
    with open(Path(dir, "result_2.json") as f:
        print(result_2, file=f)
```

## 🔐 Safe default

By default, atomik will not overwrite files/non-empty folders, but it's configurable. 

## 🕵️‍♀️ How ?

Atomik uses the new `renameat2` syscall to allow to rename file in an atomic way. While 

## Limitation

The syscall doesn't allow to overwrite a non-empty folder when renaming. 
This is achieved using the `exchange` flag to swap the two folder and then the source
folder is cleaned. This may leave the `src` folder in case of interruption/issue when deleting
but the destination folder will still be written in an atomic way.
