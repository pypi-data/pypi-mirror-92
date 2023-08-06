# dirganize

A command-line tool to organize files into category directories.

## Installation

```shell
pip install dirganize
```

## Usage

Move into your desired directory and run `dirganize`.

It will put all files into their respective category folders, based on the default configuration.

You can put a `.dirganize.yml` file ( inside the folder you want to dirganize ) to override the default configuration.

<details>
<summary> See the default configuration  </summary>

```yaml
android:
  - apk

animations:
  - gif

archives:
  - zip
  - tar
  - gz

configs:
  - yaml
  - ini
  - env
  - yml

databases:
  - csv
  - xlsx
  - xls
  - db

docs:
  - pdf
  - txt
  - md

ebooks:
  - epub

images:
  - png
  - jpg
  - jpeg

scripts:
  - py
  - sh
  - java
  - cpp
  - c
  - js

videos:
  - mp4
  - webp

webpages:
  - html

```

</details>

Basically you have the folder name, followed by file types to put in that folder.

You can also specify which folder to organize:

```shell
dirganize --path ~/Downloads
```

