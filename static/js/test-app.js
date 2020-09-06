const loginBtn = $('#btn-login');
const logoutBtn = $('#btn-logout');
// const backBtn = $('.back');
// const moviesBtn = $('#movies');
// const actorsBtn = $('#actors');
// const frontCon = $('#front-container');
// const gatedCon = $('#gated-content');
// const moviesCon = $('#movies-container');
// const actorsCon = $('#actors-container');
// const accessTokenCon = $('#access-token-container');

let auth0 = null;
/**
 * 
 * 
 * REMOVE IN PRODUCTION
 *
 *
 */
// let isAuthenticated = false; 

// const fetchAuthConfig = () => fetch('static/auth_config.json');
const configureClient = async()=> {
    const response = await fetch('static/auth_config.json');
    const config = await response.json();
    // console.log('config client:',config);
    auth0 = await createAuth0Client({
        domain: config.domain,
        client_id: config.clientId,
        audience: config.audience
    });
};

window.onload = async()=> {
    await configureClient();
	const isAuthenticated = await auth0.isAuthenticated();
    updateUI();

    const query = window.location.search;
    if(query.includes('code=') && query.includes('state=')) {
        await auth0.handleRedirectCallback();
        updateUI();
        window.history.replaceState({}, document.title, '/');
    }
};

const updateUI = async()=> {
    const isAuthenticated = await auth0.isAuthenticated();
    console.log(isAuthenticated);
    if(isAuthenticated){
        loginBtn.addClass('hidden');
        logoutBtn.removeClass('hidden');
        console.log(await auth0.getTokenSilently());
    } else {
        loginBtn.removeClass('hidden');
        logoutBtn.addClass('hidden');
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

