const express = require('express');
const router = express.Router()

const { spawn } = require('child_process');
const { response } = require('express');

// Full path to the Python executable
const pythonExecutable = '/opt/homebrew/bin/python3'; // Change this to the actual path

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

// Getting api help
router.get('/', (request, response) => {
    const api_document_text = '{ "API\'s" : [' +
    '{ "API syntax":"/api/news" , "description":"Returns JSON format of top news" },' +
    '{ "API syntax":"/api/name" , "description":"Returns JSON format of top ranked players" },' +
    '{ "API syntax":"/api/rank?val1=[rank1]&val2=[rank2]" , "description":"Retruns JSON format of win rate calculation of player [rank1] vs player [rank2]" },' +
    '{ "API syntax":"/api/name?val1=[name1]&val2=[name2]" , "description":"Retruns JSON format of win rate calculation of player [name1] vs player [name2]" } ]}';
    const api_document_json = JSON.parse(api_document_text);

    response.send(api_document_json);
});

router.get('/document', (request, response) => {
    response.redirect('/api');
});

// Getting news json
router.get('/news', async (request, response) => {
    try {
        result = await executePython('src/web_crawling/news.py', []);
        console.log(result)
        response.send(result);
    } catch (error) {
        response.status(500).json({ error: error });
    }
});

// Getting victory rate
router.get('/victory_rate_calculator/:id', async (request, response) => {
    flag = request.params.id
    const queryString = request.url.split('?')[1];
    const params = {};
    if (queryString) {
        const queryParams = queryString.split('&');
        queryParams.forEach(param => {
            const [key, value] = param.split('=');
            params[key] = value;
        });
    }

    val1 = params['val1']
    val2 = params['val2']

    if(val1 == undefined) {
        try {
            result = await executePython('tennis_return.py', [flag]);
            // console.log(result)
            response.json({ result:result });
        } catch (error) {
            response.status(500).json({ error: error });
        }
    }

    else {
        try {
            result = await executePython('tennis_pythagorean.py', [flag, val1, val2]);
            // console.log(result)
            response.json({ result:result });
        } catch (error) {
            response.status(500).json({ error: error });
        }
    }
});

module.exports = router

