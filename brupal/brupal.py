#!/usr/bin/env python

import os
from optparse import OptionParser
import subprocess
from subprocess import call

usage = "Usage: %prog [options] mysql-database mysql-username [mysql-password]"
parser = OptionParser(usage=usage)
parser.add_option("-d", "--directory", action="store", type="string", dest="drupal_directory", default="./drupal", help="specify a directory to install Drupal into. Default directory is ./drupal")
parser.add_option("-H", "--host", action="store", type="string", dest="mysql_host", default="127.0.0.1", help="MySQL hostname or IP address. Defaults to 127.0.0.1.")

(options, args) = parser.parse_args()

if len(args) < 2:
  parser.error("you must supply a MySQL database and username.")
elif len(args) == 2:
  args.append("")

def delete_drupal_directory(drupal_directory):
  call(["rm", "-fr", "%s" % drupal_directory])

# TODO: Add support for detecting and destroying existing MySQL database

# if args[2] == "":
#   args[2] = '""'

# p = subprocess.call(["mysql", "-u", args[1], '--password', args[2], "-e", '"SHOW TABLES FROM %s"' % args[0], args[0]])

# print p
# for line in p.stdout.readlines():
#   print line

print "Brupal v0.1.1"

if options.drupal_directory != "." and os.path.exists(options.drupal_directory):
  print "Deleting directory '%s'..." % options.drupal_directory
  delete_drupal_directory(options.drupal_directory)
elif options.drupal_directory == ".":
  print "Using the current directory."

  if os.path.exists("./sites"):
    print "It appears there is an existing Drupal installation in the current directory. Please clean out the current directory and try again."
    quit()

print "Setting up a new Drupal install in %s..." % options.drupal_directory

print "Downloading Drupal and module files..."

call(["drush", "make", "--working-copy", "--no-gitinfofile", "janrain_dev.make", options.drupal_directory])

print "Copying install profile to the Drupal installation..."

call(["cp", "-R", "janrain_dev", "%s/profiles/janrain_dev" % options.drupal_directory])

print "Performing a site install..."

#call(["cd", "%s" % options.drupal_directory])
os.chdir(options.drupal_directory)
call(["drush", "si", "janrain_dev", "--db-url=mysql://%s:%s@%s/%s" %(args[1], args[2], options.mysql_host, args[0]), "-y"])