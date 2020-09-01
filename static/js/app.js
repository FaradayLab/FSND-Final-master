let auth0 = null;

$("#btn-logout").addClass("hidden");
$("#movies").addClass("hidden");
$("#actors").addClass("hidden");
$("#back").addClass("hidden");
$("#movies-container").hide();
$("#actors-container").hide();


const fetchAuthConfig = () => fetch("static/auth_config.json");
const configureClient = async () => {
    const response = await fetchAuthConfig();
    const config = await response.json();
  
    auth0 = await createAuth0Client({
      domain: config.domain,
      client_id: config.clientId,
      audience: config.audience
    });
  };

window.onload = async () => {
    await configureClient();
    updateUI()

    const isAuthenticated = await auth0.isAuthenticated();
    console.log(isAuthenticated)
    if(isAuthenticated){
        $("#btn-login").addClass("hidden");
        $("#btn-logout").removeClass("hidden");
        $("#movies").removeClass("hidden");
        $("#actors").removeClass("hidden");
        $("#btn-login").prop("disabled", false);
        $("#btn-logout").prop("disabled", true);
    }

    else{
      $("#btn-login").prop("disabled", false);
    }
    const query = window.location.search;
    if (query.includes("code=") && query.includes("state=")) {
    
        await auth0.handleRedirectCallback();
        updateUI();
        window.history.replaceState({}, document.title, "/");
    }
};

const updateUI = async () => {
    const isAuthenticated = await auth0.isAuthenticated();
  
    document.getElementById("btn-logout").disabled = !isAuthenticated;
    document.getElementById("btn-login").disabled = isAuthenticated;

    if(isAuthenticated){
        $("#btn-login").hide();
        $("#gated-content").removeClass("hidden");
        $("#ipt-access-token").html(await auth0.getTokenSilently());
        $("#movies").prop("disabled", false);
        $("#actors").prop("disabled", false);
        $("#btn-login").prop("disabled", false);
        $("#btn-logout").prop("disabled", true);
        $("#btn-logout").removeClass("hidden");
        $("#movies").removeClass("hidden");
        $("#actors").removeClass("hidden");
    }
};

const login = async () => {
    await auth0.loginWithRedirect({
      redirect_uri: window.location.origin
    });
};

const logout = () => {
    auth0.logout({
      returnTo: window.location.origin
    });
};
const back = async (event) => {
    auth0.logout({
      returnTo: window.location.origin
    });
  }

const movies = async () => {
  const accessToken = await auth0.getTokenSilently();
  $("#movies-container").show()
  $("#gated-content").addClass("hidden");
  $("#btn-logout").addClass("hidden");
  $("#actors").addClass("hidden");
  $("#movies").addClass("hidden");
  $("#back").removeClass("hidden");
  $("#head").removeClass("container");
  $(".container").hide();

  $.ajax({
      method: 'GET',
      url: 'https://fsndfinal.herokuapp.com/movies',
      headers: {
        Authorization: 'Bearer ' + accessToken
      },
      success: function(movie){
        movie[0].movies.forEach(function(m){
           
            $("<h3>").appendTo("#movies-container").text("Title: "+m.title);
            $("<h5>").appendTo("#movies-container").text("Release Date: "+m.release_date)
            $("<h5>").appendTo("#movies-container").text("Id: "+m.id)
        });
      }
  });
}

const actors = async () => {
    const accessToken = await auth0.getTokenSilently();
    $("#movies-container").hide()
    $("#gated-content").addClass("hidden");
    $("#btn-logout").addClass("hidden");
    $("#actors").removeClass("hidden");
    $("#movies").addClass("hidden");
    $("#back").removeClass("hidden");
    $("#head").removeClass("container");
    $(".container").hide();
    $("#actors-container").show();

  
    $.ajax({
        method: 'GET',
        url: 'https://fsndfinal.herokuapp.com/actors',
        headers: {
          Authorization: 'Bearer ' + accessToken
        },
        success: function(actor){
          actor[0].actors.forEach(function(actor){
             
              $("<h3>").appendTo("#actors-container").text("Name: "+actor.name);
              $("<h5>").appendTo("#actors-container").text("Age: "+actor.age)
              $("<h5>").appendTo("#actors-container").text("Gender: "+actor.gender)
              $("<h5>").appendTo("#actors-container").text("Id: "+actor.id)
          });
        }
    });
  }
