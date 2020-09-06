const loginBtn = document.querySelector('#btn-login');
const logoutBtn = document.querySelector('#btn-logout');
let auth0 = null;

const configureClient = async()=> {
    const response = await fetch('static/auth_config.json');
    const config = await response.json();
    auth0 = await createAuth0Client({
        domain: config.domain,
        client_id: config.clientId,
        audience: config.audience
    });
};

const updateUI = async()=> {
    const isAuthenticated = await auth0.isAuthenticated();
    if(isAuthenticated){
        loginBtn.classList.add('hidden');
        logoutBtn.classList.remove('hidden');
        console.log(await auth0.getTokenSilently());
    } else {
        loginBtn.classList.remove('hidden');
        logoutBtn.classList.add('hidden');
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