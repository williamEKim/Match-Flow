const express = require ('express');

// express app
const appInstance = express();

// register view engine
appInstance.set('view engine', 'ejs');
    // folder configuration
    appInstance.set('views', 'views')

// listen for request
appInstance.listen(3300);

appInstance.get('/', (request, response) => {
    // const blogs = [
    //     { title: 'post 1', snippet: '1' },
    //     { title: 'post 2', snippet: '2' },
    //     { title: 'post 3', snippet: '3' }
    // ]

    response.render('index', {
        title: "Home",
        // blogs
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