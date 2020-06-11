# CanDIG-Server Dashboard

The candig-server dashboard is composed of two major components. The internal JavaScript and CSS that implement the charting, basic interaction, form rendering, as well as the integration of the IGV Browser (under /core), and the external paper-dashboard styling (under /assets).

# Core

This directory contains the core static files to render the dashboard. You need to have npm installed in order to compile the JavaScript (in ES 6 Syntax).

Assume you are at directory `static/core/js`, in order to minify the Javascript, run

```
npm install babel-minify --save-dev

npm install @babel/preset-env --save-dev

npx babel src --watch --out-dir dist

```


# Assets

This directory contains the external assets from paper-dashboard. 