# Moodle Update Script
This script is used to update Moodle to the latest version including used plugins.
The script utilizes the moodle api endpoints found in
```/lib/classes/update/api.php``` and ```/lib/classes/update/checker.php``` to fetch and download the newest stable moodle
versions and their corresponding plugins. Optionally it can automatically apply core changes
(custom changes to moodle or plugin core files).

## Requirements
This script requires a Python-3 installation and all the packages listed in the `requirements.txt` file.
Plugins are defined in the `plugin_list` array (Frankenstein component names).
## Usage
To use the script, run it from the command line with `python3 main.py` or `py main.py`.
The user can choose to update to the latest stable version, the latest development version, or the newest "Other supported release".
The output is a complete moodle directory with the chosen version and all version compatible plugins.  
![moodle-update-script-output](https://github.com/user-attachments/assets/397795ce-f673-4c23-bb54-5d923086af25)


### corechanges
Corechanges are custom changes to the Moodle or plugin source code.
To apply core changes, the script will look for files in the `corechanges` directory.

Each changed moodle file exists of two files in this script - the original file as it is in the Moodle source code and the modified file.
The original file has the suffix `.default` while the modified file has no suffix.
Eg.  
`mod-assign-submission-file.php.default` and  
`mod-assign-submission-file.php`.  
The names of the files are the folder structure where the files would be located in the Moodle source code, separated by dashes.  
The script creates a sha256 checksum of the original file (default suffix) and compares it to the checksum of the equal Moodle file.
If the checksums match, the script replaces the original file with the modified file, since the file has not changed.

## TODO
- [ ] better error handling
- [ ] implementation of automatic deployment of corechanges
