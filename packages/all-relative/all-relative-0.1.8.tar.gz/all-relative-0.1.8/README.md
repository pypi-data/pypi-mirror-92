# all-relative

A command line tool to convert a static site to use only relative urls.

Run it from the the directory which contains your generated static site to have it convert all urls in html and css to be relative to that dir or specify it as a cli argument.

Relative urls leaves you with a portable website that doesn't care what path it is mounted at. `/`, `/olizilla/` `/ipfs/hash/`, `file://x/y/z/`, the lot, it don't care. This allows you to load the same static site via [IPFS](https://ipfs.io) or github pages, or the localfile system, as well as from the root of your custom domain. Relative urls are wonderful.

The command will **edit the files in place**, so it's best to run it on generated output that you can recreate if you need to. If you can't, be sure to take a back up of your site first.

## Install

Install it with 

```console
$ pip install all-relative
```

or run just it wihtout installing it via `pipx` [see here if you haven't heard about it](https://github.com/pipxproject/pipx)

```console
$ pipx all-relative
```

## Usage

Run the command from the root directory of your static site.

```console
$ all-relative
```

# Inspired by [all-relative](https://github.com/olizilla/all-relative)