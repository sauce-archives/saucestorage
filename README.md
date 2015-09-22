# saucestorage

Simple Python interface and command-line tool to the `sauce-storage` API of Sauce Labs.

## Synopsis

``` bash
$ saucestorage list 
   2069068  Sep 19 2015 01:15:21  Sample.ipa 

$ saucestorage put MyApp.apk

$ saucestorage list
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

Another option is to use the Sauce Storage API. You upload the file once to Sauce Storage,
and when your test wants it, it's already right there, in Sauce Labs' network.

In the example in the Synopsis, the user wants to test the Android app `MyApp.apk`. She
uploads it as shown, and then, in the `capabilities` for her tests,
she refers to the app as `sauce-storage:MyApp.apk`.

You can already use Sauce Storage with a simple `curl` command, but this utility should make it 
a bit easier.

#### iOS Real Device Cloud

For tests that use the Sauce Labs iOS Real Device Cloud, you *must* upload your app
to Sauce Storage first, and refer to it in the test capabilities with a `sauce-storage:` URL.

## Getting started

You'll need to be familiar with running scripts on the command line, and have
Python 2.x or better installed.

First you'll need a couple of environment variables. `SAUCE_USERNAME` should be the 
username you use to log into [https://saucelabs.com/](http://saucelabs.com/). Your 
*access key* is available in your User Settings page. (Click on your username in the 
Sauce Labs web interface to find the settings. Your access key should be a long string
of numbers, letters, and dashes.)

```
$ export SAUCE_USERNAME=your_username
$ export SAUCE_ACCESS_KEY=your_access_key
```

You might want to add these lines to your shell's startup profile, which for most people
is in their home directory under `.bash_profile`.

Next, just install this package with `pip`:

``` bash
$ pip install saucestorage
```

Then, the `saucestorage` program should be installed for you, and you can invoke it 
as in the Synopsis above.

## Command-line options

`saucestorage` has two main functions: `list` and `put`. 

### list

```
saucestorage list [-h] [-v] [-d]

List files in storage using Sauce Labs Storage API.

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Extra logging
  -d, --data     Print results as python data structure
```

By default, `list` shows you several columns: the size of the file in bytes, the 
date uploaded, and the file name.


### put
```
saucestorage put [-h] [-v] [-d] [-c] [-n NAME] <path>

Put a file into storage using Sauce Labs Storage API.

positional arguments:
  <path>                File to upload

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Extra logging
  -d, --data            Print results as python data structure
  -c, --checkhash       Check hash after upload
  -n NAME, --name NAME  Store file with this filename
```

The `--name` argument allows you to store a file under a different
name than what it has on your filesystem. For instance:

``` bash
$ saucestorage put -n RemoteName.zip /path/to/LocalName.zip

$ saucestorage list
   4417873  Sep 19 2015 01:20:55  RemoteName.zip
```

The `--checkhash` argument will double check that the uploaded file
has the exact same contents as the original. Normally this is silent;
it will only warn you if they are different.

## Python library

`saucestorage` also includes a Python library you can use, to script your own tests.

You can use it like this:

``` python
storage_api = SauceStorageClient(username='your_user_name',
                                 access_key='your_access_key')
file_list = storage_api.list()
for f in file_list:
    print f['name']

storage_api.put('/Users/me/SomeApp.ipa')
```

## Limitations of the Sauce Storage API

You cannot download files from your Sauce Storage area, nor can you delete files. 

Files will be retained for about a week. 

See the [Sauce Labs Storage API documentation](https://docs.saucelabs.com/reference/rest-api/#temporary-storage) 
for more information.
