# yum-install-blacklist

yum plugin to allow certain RPMs to only be upgraded, and not installed.

Addresses issue where you dont want any further new installs of a product, yet you want
existing versions to get happily patched if required.


## Example

### Create repo with blacklist tag, blacklisting ImageMagick and microsoft

````
$ sudo createrepo --content=blacklist:^ImageMagick,^microsoft /var/www/html/repo
Spawning worker 0 with 25 pkgs
Workers Finished
Gathering worker results

Saving Primary metadata
Saving file lists metadata
Saving other metadata
Generating sqlite DBs
Sqlite DBs complete
$
````

### Query repo to determine blacklist details

````
$ yum repolist -v|grep ^Rep
Repo-id      : steve-repo
Repo-name    : Steve repo
Repo-revision: 1463431538
Repo-tags    : blacklist:^ImageMagick,^microsoft
Repo-updated : Mon May 16 13:45:39 2016
Repo-pkgs    : 23
Repo-size    : 33 M
Repo-baseurl : http://192.168.0.20/repo
Repo-expire  : 21,600 second(s) (last: Mon May 16 13:45:50 2016)
Repo-excluded: 2
$
````

### List ImageMagick rpms in repo

````
$ sudo yum -q --showduplicates list ImageMagick*
Error: No matching Packages to list
$ sudo yum --disableplugin=install-blacklist -q --showduplicates list ImageMagick*
Available Packages
ImageMagick-last-doc.x86_64                                     6.9.3.10-1.el6.remi                                      steve-repo
ImageMagick-last-doc.x86_64                                     6.9.4.1-1.el6.remi                                       steve-repo
$
````

### Install old version of ImageMagick

````
$ sudo yum -q install ImageMagick-last-doc-6.9.3.10
Error: Nothing to do
$ sudo yum --disableplugin=install-blacklist -q install ImageMagick-last-doc-6.9.3.10

===================================================================================================================================
 Package                              Arch                   Version                              Repository                  Size
===================================================================================================================================
Installing:
 ImageMagick-last-doc                 x86_64                 6.9.3.10-1.el6.remi                  steve-repo                 4.7 M

Transaction Summary
===================================================================================================================================
Install       1 Package(s)

Is this ok [y/N]: y
$
````

### Upgrade to new version of ImageMagick

````
$ sudo yum -q upgrade ImageMagick-last-doc

===================================================================================================================================
 Package                              Arch                   Version                              Repository                  Size
===================================================================================================================================
Updating:
 ImageMagick-last-doc                 x86_64                 6.9.4.1-1.el6.remi                   steve-repo                 4.7 M

Transaction Summary
===================================================================================================================================
Upgrade       1 Package(s)

Is this ok [y/N]: y
$ rpm -q ImageMagick-last-doc
ImageMagick-last-doc-6.9.4.1-1.el6.remi.x86_64
$
````

## Files

* /etc/yum/pluginconf.d/install-blacklist.conf
````
    [main]
    enabled=1
````
* /usr/lib/yum-plugins/install-blacklist.py
