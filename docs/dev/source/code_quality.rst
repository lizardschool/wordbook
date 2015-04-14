Code quality
============


Java Script
-----------

.. code-block:: sh

   npm install jslint
   find wordbook/flaskapp/static -iname "*.js"|xargs node node_modules/jslint/bin/jslint.js
