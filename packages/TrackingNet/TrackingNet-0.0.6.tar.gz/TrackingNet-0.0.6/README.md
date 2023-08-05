# TrackingNet

This repo is a Github Project Page.

- The website is hosted on the `docs` folder.

- The hugo source code is available on the `hugo` folder.

- The pip source code is available on the `TrackingNet` folder.

## Website

### Test

Modify the hugo source files and use `./hugo_mac server`  on the hugo folder to see the updates locally on `http://localhost:1313/TrackingNet/`

### Deploy

A bash script automatize the website deployement on mac `./deploy_mac.sh`

- Generate the new website in the `docs\` folder using `./hugo_mac`.

- Create the CNAME for `tracking-net.org`

- Push your modification on Github:

`git pull`

`git add .`

`git commit -am "commit message"`

`git push`

## pip package

```bash
conda create -n TrackingNet python pip
pip install TrackingNet

pip install twine
pip install scikit-video
pip install pyocclient
```
