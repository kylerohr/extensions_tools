#!/bin/bash

drupaldir="drupal"

echo 'Setting up a new Janrain Dev Drupal install in ./drupal...'

if [ -d ./$DRUPALDIR ]; then
  echo 'Drupal directory exists.'
  echo 'Deleting Drupal directory...'

  sudo rm -rf drupal
fi

echo 'Downloading Drupal and module files...'

drush make --working-copy --no-gitinfofile janrain_dev.make drupal

echo 'Copying install profile to new Drupal directory...'

cp -R janrain_dev drupal/profiles/janrain_dev

echo 'Installing Janrain Dev site...'

cd drupal

drush si janrain_dev --db-url=mysql://$1:$2@127.0.0.1/$3 -y