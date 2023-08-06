[![img](https://img.shields.io/badge/Made_in-VSCode-blue?style=for-the-badge)](https://code.visualstudio.com/download)
[![img](https://img.shields.io/badge/follow_me-@alka1e-E4405F?style=for-the-badge&logo=instagram&labelColor=8f3c4c&logoColor=white)](https://www.instagram.com/alka1e)
[![img](https://img.shields.io/badge/follow_me-@alka1e-1DA1F2?style=for-the-badge&logo=twitter&labelColor=27597a&logoColor=white)](https://twitter.com/alka1e)

# Ddot

_Your dev environment manager_

[![img](https://img.shields.io/badge/work_in-progress-eb3434?style=for-the-badge&labelColor=7d1616)]()
[![img](https://img.shields.io/badge/license-mit-blueviolet?style=for-the-badge)]()

----

[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/uses-git.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/built-by-hipsters.svg)](https://forthebadge.com)


[[_TOC_]]

# Introduction 

Ddot is a devinstaller application created using the devinstaller framework.

[For more info read below](#what-is-devinstaller)

# Getting Started

```sh
pipx run ddot run
```

There needs to be a devfile in the current directory. Any one of these:

- `devfile.toml`
- `devfile.yaml` or `devfile.yml`
- `devfile.json`

# Installation

There are two method to use the application:
1. Using Pipx to directly run the application 
2. Installing the application on your machine

Using [Pipx](https://github.com/pipxproject/pipx) method is recommended.

## Method 1: Using Pipx

Why this method is recommended?

You can use Pipx to directly run the latest version of ddot without installing it in your machine. This way
your machine stays clean and you don't need to worry about updating ddot.

You can also install ddot in your machine using pipx if that's what you want.

### Usage without installation

1. Install pipx

- On MacOS
```sh
brew install pipx
pipx ensurepath
```
-  Other OS

```sh
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

for more information check out [Pipx](https://github.com/pipxproject/pipx).

2. Using ddot

```sh
pipx run ddot <command> # Example: pipx run ddot run --verbose
```

Please note that the commands in the section below will need the `pipx run ` prefix with this method. Other method
doesn't require this prefix.

### Usage with installation

```sh
pipx install ddot
```

## Method 2: Machine installation

You can also install ddot without pipx. Although this is discouraged as ddot may disturb your system packages.

```sh
python -m pip install ddot
```

# Commands

- Show the ddot version
```sh
ddot --version
```

- Show the help menu
```sh
ddot --help
```

- Show all the modules available in the devfile
```sh
ddot show
```

- Execute the modules

```sh
ddot run
```

This command will open up a interactive prompt which you can use to navigate and select all the modules you want to execute.

You select modules using your SPACEBAR key and naviage using your ARROW keys.

- You can also skip the interactive prompt by running

```sh
ddot run -m <module name>
```

Here `<module name>` is the name of the module in the devfile at the current directory.

- You can also specify the location to the devfile if it's not present in the current directory or if it's named differently

```sh
ddot run --spec-file <spec file location>
```

- You can also set the verbose flag using

```sh
ddot run --verbose
```

By default the verbose mode is disabled, so you won't see any of the commands that are being executed but instead will see a 
progress bar.

But if you need to see it just run using the verbose flag.

# What is Devinstaller?

Devinstaller is a framework to execute the devfiles.

# What are devfiles?

Devfiles is made up of 2 file:
1. Spec file
2. Prog file

## Spec file?

The guiding principle behind the Spec file is to give a declarative and a platform agnostic way to specify a task which then can be handled by the 
devinstaller application and make that happen.

In Devinstaller the basic building block for anything is called a "module".

And you execute/install the module to do something.

### Modules

We have modules for:
1. file
2. folder
3. link
4. app
5. phony
6. group

    - `file`, `folder` and `link` modules
        Say you want to create a file in a declarative way. For this you use the file module
        and specify where and what the file is and the devinstaller will handle how to create/update/delete
        the file.

        This way your file module is declarative and the application handles everything required to make it happen, 
        including on how to do it on different OS.

        This is how the `file`, `folder` and the `link` module works.

    - `app` module
        Then we have the `app` module. App module is for system applications. Here you need to write in some imperative instructions on how
        a specific application is to be installed. But the beauty behind this you can add in instructions on how to do the same on different
        platforms and the overall module becomes declarative for other users.

        Example: You can write up the instructions to install ddot on different OS in a devfile, which an another user can import the devfile into
        their devfile and it will give them a declarative way to install ddot on their machine and they don't have to worry about how it's going to
        be done.

    - `phony` and `group` module
        But we understand that not everything can be put in a declarative way so for those cases we have the `group` and the
        `phony` module. You can combine these modules in any fashion to translate your imperative instructions into a more
        declarative way.

### dGenerate
For writing up spec file you can use the web application [dGenerate](https://dgenerate.aziraz.com/) or you can write it in any text editor.

Using dGenerate will give you better user experience. 

- Features of dGenerate 

    1. Write and save in any file format.
        Formats supported include:
        - TOML
        - YAML
        - JSON

    2. You can upload existing devfile and do some changes and download it.
    3. You can share the link to your dGenerate devfile and send it to anyone. And they can go to the link make their changes and download it.
    4. dGenerate is a completely offline application and it doesn't send any data to any servers.
        So you can be assured of the safety of your data. Even for generating the share link for your devfile, we don't store any data on any server.
        All the data required are in the link itself. You might have probably noticed that all the share links are unusually long and now
        you know the reason for it.

## Prog file?

TODO

# License

MIT License

Copyright (c) 2021 Justine Kizhakkinedath

