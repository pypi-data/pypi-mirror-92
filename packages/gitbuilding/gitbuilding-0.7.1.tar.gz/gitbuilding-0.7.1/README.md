# What is GitBuilding

GitBuilding is a program for documenting hardware. The goal of GitBuilding is to give you the freedom to write instructions in the form and structure that you want using markdown. Some extra syntax is added to generate the difficult things like bills of materials.

In GitBuilding you are able to:

* Write the instructions as you go along in markdown
* Tag links in the code with meta-data to show if they are steps in the build or parts that are needed
* Define a library including the part numbers for multiple suppliers
* Syntax for adding in bill of materials

**Note: While we work out the best syntax, major things might change!** If you have syntax suggestions please raise an issue!

To find out more [**visit our website**](https://gitbuilding.io/).


# How to install/use GitBuilding

To install (for Python 3.6+)

    pip install gitbuilding
    
[More details are available on the website.](https://gitbuilding.io/software)

### Installing the Dev package

We sporadically we build dev packages for testing. We don't recommend this for normal use and cannot promise features in it work. But it can be useful for testing.

Dev packages are stored on our [internal package registry](https://gitlab.com/groups/gitbuilding/-/packages). To install them you will need a GitLab account and to make an access token.

**To make the token:**

* Log in to GitLab and go to your settings
* Select "Access Tokens" on the left menu
* Create a "Personal Access Token" with "real_api" scope
* Save this token for later

**To install the dev package:**

Download the wheel with:
```
pip download gitbuilding --no-deps --index-url https://__token__:<YOUR-TOKEN>@gitlab.com/api/v4/projects/9353371/packages/pypi/simple
```
replacing `<YOUR-TOKEN>` with your personal access token.

Then install with:
```
pip install gitbuilding*.whl
```

### Installing from source
If you wish to contribute to development of GitBuilding you can clone the project like normal but you may need to build the javascript editor from source. To do so please see the [contribution page](https://gitlab.com/gitbuilding/gitbuilding/-/blob/master/CONTRIBUTING.md) and the [developer installation instructions](https://gitlab.com/gitbuilding/gitbuilding/-/blob/master/DeveloperInstallation.md).



# Syntax for documentation

The syntax for documentation is in a format we call BuildUp. [More details are available on the website](https://gitbuilding.io/syntax/).
