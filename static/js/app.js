const loginBtn = $('#btn-login');
const logoutBtn = $('#btn-logout');
const backBtn = $('#back');
const movies = $('#movies');
const actors = $('#actors');
const movieCon = $('#movies-container');
const actorCon = $('#actors-container');
const gated = $('#gated-content');

let auth0 = null;

// const fetchAuthConfig = () => fetch('static/auth_config.json');
const configureClient = async()=> {
    const response = await fetch('static/auth_config.json');
    const config = await response.json();
    console.log('config client:',config);
    auth0 = await createAuth0Client({
        domain: config.domain,
        client_id: config.clientId,
        audience: config.audience
    });
  };

window.onload = async()=> {
    await configureClient();
    updateUI();
	
	const isAuthenticated = await auth0.isAuthenticated();
    console.log('isAuthenticated:',isAuthenticated);
    if(isAuthenticated){
        loginBtn.addClass('hidden');
        logoutBtn.removeClass('hidden');
        movies.removeClass('hidden');
        actors.removeClass('hidden');
        loginBtn.prop('disabled', true);
        logoutBtn.prop('disabled', false);
    } else {
        loginBtn.prop('disabled', false);
    }
    const query = window.location.search;
    if(query.includes('code=') && query.includes('state=')) {
    
        await auth0.handleRedirectCallback();
        updateUI();
        window.history.replaceState({}, document.title, '/');
    }
};

const updateUI = async()=> {
    console.log('updateUI');
    const isAuthenticated = await auth0.isAuthenticated();
    console.log('updateUI isAuthenticated:',isAuthenticated);

    logoutBtn.prop('disabled', !isAuthenticated);
    loginBtn.prop('disabled', isAuthenticated);
    // document.getElementById('btn-logout').disabled = !isAuthenticated;
    // document.getElementById('btn-login').disabled = isAuthenticated;

    if(isAuthenticated){
        loginBtn.addClass('hidden');
        gated.removeClass('hidden');
        $('#ipt-access-token').html(await auth0.getTokenSilently());
        movies.prop('disabled', false);
        actors.prop('disabled', false);
        loginBtn.prop('disabled', true);
        logoutBtn.prop('disabled', false);
        logoutBtn.removeClass('hidden');
        movies.removeClass('hidden');
        actors.removeClass('hidden');
    }
};

const login = async()=> {
    await auth0.loginWithRedirect({
      redirect_uri: window.location.origin
    });
};
const logout =()=> {
    auth0.logout({
      returnTo: window.location.origin
    });
};
const back = async()=> {
    auth0.logout({
      returnTo: window.location.origin
    });
};

const fetch_movies = async() => {
    const accessToken = await auth0.getTokenSilently();
    movieCon.show();
    gated.addClass('hidden');
    logoutBtn.addClass('hidden');
    movies.addClass('hidden');
    actors.addClass('hidden');
    backBtn.removeClass('hidden');
    $('#head').removeClass('container');
    $('.container').hide();

    $.ajax({
        method: 'GET',
        url: 'https://alex-fsnd-capstone.herokuapp.com/movies',
        headers: {
            Authorization: 'Bearer ' + accessToken
        },
        success: function(movie){
            movie[0].movies.forEach(function(m){
                $('<h3>').appendTo('#movies-container').text('Title: '+m.title);
                $('<h5>').appendTo('#movies-container').text('Release Date: '+m.release_date);
                $('<h5>').appendTo('#movies-container').text('Id: '+m.id);
            });
        }
    });
};

const fetch_actors = async()=> {
    const accessToken = await auth0.getTokenSilently();
    movieCon.hide();
    gated.addClass('hidden');
    logoutBtn.addClass('hidden');
    actors.removeClass('hidden');
    movies.addClass('hidden');
    backBtn.removeClass('hidden');
    $('#head').removeClass('container');
    $('.container').hide();
    actorCon.show();
  
    $.ajax({
        method: 'GET',
        url: 'https://alex-fsnd-capstone.herokuapp.com/actors',
        headers: {
            Authorization: 'Bearer ' + accessToken
        },
        success: function(actor){
            actor[0].actors.forEach(function(actor){
                $('<h3>').appendTo('#actors-container').text('Name: '+actor.name);
                $('<h5>').appendTo('#actors-container').text('Age: '+actor.age);
                $('<h5>').appendTo('#actors-container').text('Gender: '+actor.gender);
                $('<h5>').appendTo('#actors-container').text('Id: '+actor.id);
            });
        }
    });
  };
