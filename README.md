This is a college project that ciphers text using Python's "ord" and "chr" functions and makes that functionality available in an easy to use interface.

# Breakdown
"cipher.py" holds all of the primary ciphering functions used.
"server.py" starts a local web server to display HTML visuals in a browser.
The public folder holds all files indiscriminately served by the server, which includes all HTML, CSS, and JS files/code.

# Instructions
Simply run the "server.py" file and then go to http://localhost:8080. Explore around, read up on the different cipher types, use the ciphers, and even save presets for them if you have special specific ones you want to save for later. Presets are stored through the browser's local storage and persist between server activation. Then, when you're done, close the server (e.g. Ctrl+C through a terminal or closing the IDE the code is running through.)

# Testing
If you don't want to test the ciphers, that is fine, but there are debugging tools in this project that can be used.
By running the "tests.py" file, the ciphers in the project will be tested to ensure their outputs do not give an error and that encrypted strings can be decrypted.
