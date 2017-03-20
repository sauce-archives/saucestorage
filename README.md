# saucestorage

Simple Python interface and command-line tool to the 
[Sauce Labs Storage API](https://docs.saucelabs.com/reference/rest-api/#temporary-storage). 

## Synopsis

```bash
$ saucestorage list 
      Size  Modification time     Name
      ----  -----------------     ----
   2069068  Sep 19 2015 01:15:21  Sample.ipa

$ saucestorage put MyApp.apk
File '/current/directory/MyApp.apk' is now available as sauce-storage:MyApp.apk

$ saucestorage list
      Size  Modification time     Name
      ----  -----------------     ----
   2069068  Sep 19 2015 01:15:21  Sample.ipa
  13317873  Sep 19 2015 01:20:55  MyApp.apk
```

## What's this good for?

If you run tests inside [Sauce Labs](http://saucelabs.com), sometimes you want the test 
to download a large file. For instance, when you are testing a mobile
app, the test has to obtain the app to run, such as an Android 
`.apk` or iOS `.ipa`.

You could put the app on one of your websites, but then the tests have to download the app
over and over again.

Another option is to use the 
[Sauce Labs Storage API](https://docs.saucelabs.com/reference/rest-api/#temporary-storage). You
upload the file once to Sauce Storage, and when your test wants it, it's already right 
there, in Sauce Labs' network.

In the example in the Synopsis, the user wants to test the Android app `MyApp.apk`. She
uploads it as shown, and then, in the `capabilities` for her tests,
she refers to the app as `sauce-storage:MyApp.apk`:

``` python
  capabilities = {
      "app": "sauce-storage:MyApp.apk",
      "deviceName": "Samsung Galaxy S7 Device",
      "platformName": "Android",
      "platformVersion": "6"
      # ...and so on
  }
```

You can already use Sauce Storage with a simple `curl` command, but this utility should make it 
a bit easier.

#### iOS Real Device Cloud

For tests that use the Sauce Labs iOS Real Device Cloud, you *must* upload your app
to Sauce Storage first, and refer to it in the test capabilities with a `sauce-storage:` URL.

## Getting started

You'll need to be familiar with running scripts on the command line, and have
Python 2.x or better installed.

First you'll need a couple of environment variables. 

### Environment variables

`SAUCE_USERNAME` should be the 
username you use to log into [https://saucelabs.com/](http://saucelabs.com/). 

`SAUCE_ACCESS_KEY` should be the "access key" that Sauce assigned to you. To find it, first log into
your account on the Sauce Labs website.
* If you're using the new interface (it looks blue), click on the user account in the bottom left-hand
  corner. This should pop open a menu. Click on 'User Settings'. This opens your User Settings page. 
  Scroll down to find your Access Key.
* In the old interface (it looks more red and yellow), the Access Key is in the grey column on the 
  left hand side.


#### Linux or Mac OS X users

Type these commands:

```bash
export SAUCE_USERNAME=your_username
export SAUCE_ACCESS_KEY=your_access_key
```

You might want to add these lines to your shell's startup profile, which for most people
is in their home directory under `.bash_profile`.

#### Windows users

Type these commands:

```
set SAUCE_USERNAME=your_username
set SAUCE_ACCESS_KEY=your_access_key
```

You might want to add this to your default environment variables.

### Install the Python package

Next, just install this package with `pip`:

```bash
pip install saucestorage
```

Then, the `saucestorage` program should be installed for you, and you can invoke it 
as in the Synopsis above. You can also use it from a Python script -- see below.

## Command-line options

### list

```
saucestorage list [-h] [-v] [-j]

List files in storage using Sauce Labs Storage API.

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Extra logging
  -j, --json     Print results as JSON
```

By default, `list` shows you several columns: the size of the file in bytes, the 
date uploaded, and the file name.


### put
```
saucestorage put [-h] [-v] [-j] [-n NAME] <path>

Put a file into storage using Sauce Labs Storage API.

positional arguments:
  <path>                File to upload

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Extra logging
  -j, --json            Print results as JSON
  -n NAME, --name NAME  Store file with this filename
```

The `--name` argument allows you to store a file under a different
name than what it has on your filesystem. For instance:

``` bash
$ saucestorage put -n RemoteName.apk /path/to/LocalName.apk
File '/path/to/LocalName.apk' is now available as sauce-storage:RemoteName.apk
```

### update
```
saucestorage update [-h] [-v] [-j] [-n NAME] <path>

Very similar to `put`, but it's usually better. 

This will upload the file to Sauce Storage, but only if there
isn't already a file in storage with the same name and content.

positional arguments:
  <path>                File to upload

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Extra logging
  -j, --json            Print results as JSON
  -n NAME, --name NAME  Store file with this filename
```


### verify
```
saucestorage verify [-h] [-v] [-j] [-n NAME] <path>

Checks if a local file has the same content as a file in your storage area.

positional arguments:
  <path>                Local file to compare

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Extra logging
  -j, --json            Print results as JSON
  -n NAME, --name NAME  Storage file to compare against 
```

As in `put`, the `--name` argument allows you to compare a file with a different name 
than what is on your filesystem. 

``` bash
$ saucestorage verify /path/to/YourApp.ipa 
Files match.
```


## Python library

`saucestorage` also includes a Python library you can use, to script your own tests.

You can use it like this:

``` python
from saucestorage import SauceStorage

storage = SauceStorage(username='your_user_name',
                       access_key='your_access_key')
for f in storage.list():
    print f['name']

storage_url = storage.put('/Users/me/Some App.ipa')

print storage_url   # sauce-storage:Some%20App.ipa
```

## Limitations of the Sauce Storage API

You cannot download files from your Sauce Storage area, nor can you delete files. 

Files will be retained for about a week. 

See the [Sauce Labs Storage API documentation](https://docs.saucelabs.com/reference/rest-api/#temporary-storage) 
for more information.

## Authors

Neil Kandalgaonkar <neilk@saucelabs.com>
