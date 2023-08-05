# dropbox-pi-cli
A dropbox command line tool

Before start you need to setup the envar:
```bash
export DROPBOX_ACCESS_TOKEN='YOUR AUTH TOKEN HERE'
```

### Install

after clone cd to project folder and execute
```bash
make -B build
make install
```

### Uninstall

cd to project folder and execute
```bash
make uninstall
```
## Usage
The command line is only able to upload and download from/to dropbox app folder.

### Download
```
dropbox-pi file-download [OPTIONS]

Options:
  --remote-path TEXT  The path of the file to download.
  --local_path TEXT   The path of the file on the local moachine.
  --help              Show this message and exit.
```

### Upoload
```
dropbox-pi file-upload [OPTIONS]

Options:
  --remote_path TEXT      Path in the user's Dropbox to save the file
  --local-path TEXT       Path in the user's local to save the file
  --mode TEXT             Selects what to do if the file already exists. The
                          default for this union is add

  --autorename TEXT       If there's a conflict, as determined by mode, have
                          the Dropbox server try to autorename the file to
                          avoid conflict. The default for this field is False.

  --mute TEXT             Normally, users are made aware of any file
                          modifications in their Dropbox account via
                          notifications in the client software. If true, this
                          tells the clients that this modification shouldn't
                          result in a user notification. The default for this
                          field is False

  --strict-conflict TEXT  Be more strict about how each WriteMode detects
                          conflict. For example, always return a conflict
                          error when mode = WriteMode.update and the given
                          'rev' doesn't match the existing file's 'rev', even
                          if the existing file has been deleted. This also
                          forces a conflict even when the target path refers
                          to a file with identical contents. The default for
                          this field is False

  --help                  Show this message and exit.

```
