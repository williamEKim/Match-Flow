const express = require ('express');
const favicon = require('serve-favicon');
const { spawn } = require('child_process');
const { result } = require('lodash');

// express app
const appInstance = express();

// register view engine
appInstance.set('view engine', 'ejs');
// views folder configuration
appInstance.set('views', 'views');

// Full path to the Python executable
const pythonExecutable = '/opt/homebrew/bin/python3'; // Change this to the actual path

// const childPython = spawn(pythonExecutable, [`--version`]);

// childPython.stdout.on('data', (data) => {
//     console.log(`stdout: ${data}`);
// });

// childPython.stderr.on('data', (data) => {
//     console.error(`stderr: ${data}`);
// });

// childPython.on('error', (error) => {
//     console.error(`Error spawning Python: ${error.message}`);
// });

// childPython.on('close', (code) => {
//     console.log(`Python process exited with code ${code}`);
// });



// path configuration
// appInstance.use(express.static('public'));

const executePython = async (script, args) => {
    const arguments = args.map(arg => arg.toString());

    // const py = spawn("python", [script, ...arguments]);
    const py = spawn(pythonExecutable, [script, ...arguments]);

    const result = await new Promise((resolve, reject) => {
        let output;

        // Get output from python script
        py.stdout.on('data', (data) => {
            console.log(`stdout: ${data}`);
            output = JSON.parse(data);
        });

        // Handle erros
        py.stderr.on("data", (data) => {
            console.error(`[python] Error occured: ${data}`);
            reject(`Error occured in ${script}`);
        });

        py.on("exit", (code) => {
            console.log(`Child process exited with code ${code}`);
            resolve(output);
        });
    });

    return result;
}

// favicon configuration
appInstance.use(favicon(__dirname + '/images/icons.ico/favicon.ico'));

// listen for request
appInstance.listen(3300);

appInstance.get('/', async (request, response) => {
    let result;
    try {
        result = await executePython('src/web_crawling/news.py', []);
    } catch (error) {
        response.status(500).json({ error: error });
    }

    response.render('index', {
        title: "Home",
        result
    });


});

appInstance.get('/about', (request, response) => {
    response.render('about', {
        title: "About"
    });
});

appInstance.get('/blogs/create', (request, response) => {
    response.render('create', {
        title: "Create Post"
    });
});

// redirection
appInstance.get('/about-us', (request, response) => {
    response.redirect('/about');
});

// 404 page (default case)
appInstance.use((request, response) => {
    response.status(404).render('404', {
        title: "404 Not Found"
    });
});


// APIs
appInstance.get('/api/topnews', async (request, response) => {
    try {
        const result = await executePython('python/script.py', [8, 5]);

        response.json({ result: result });
    } catch (error) {
        response.status(500).json({ error: error });
    }

    response.json({result: result});
});