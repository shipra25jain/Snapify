// client-side js
// run by the browser each time your view template is loaded
/*
$(function() {

  $('form').submit(function(event) {
    event.preventDefault();
    
    $('#new-releases').empty();
    let country = $('select').val();
    
    // Send a request to our backend (server.py) to get new releases for the currently selected country
    $.get('/new_releases?' + $.param({country: country}), function(new_releases) {
      
      // Loop through each album in the list
      new_releases.albums.items.forEach(function(release) {
        
        // Use the returned information in the HTML
        let div = $('<div class="sp-entity-container"><a href="' + release.external_urls.spotify + 
                '"><div style="background:url(\'' + release.images[0].url + 
                '\')" class="sp-cover" alt="Album cover"></div></a><h3 class="sp-title">' + release.name + 
                '</h3><p class="text-grey-55 sp-by">By ' + release.artists[0].name + '</p></div>')
        
        div.appendTo('#new-releases')
        
      });
    });
  });

});
*/

console.log("Hello");

// Get the hash of the url
const hash = window.location.hash
.substring(1)
.split('&')
.reduce(function (initial, item) {
  if (item) {
    var parts = item.split('=');
    initial[parts[0]] = decodeURIComponent(parts[1]);
  }
  return initial;
}, {});
window.location.hash = '';

// Set token
let _token = hash.access_token;

const authEndpoint = 'https://accounts.spotify.com/authorize';

// Replace with your app's client ID, redirect URI and desired scopes
const clientId = 'a07069568b97405a9df92518444b5245';
const redirectUri = 'https://buttercup-visage.glitch.me/';
const scopes = [
  'playlist-modify-private',
  'user-modify-playback-state'
];

// If there is no token, redirect to Spotify authorization
if (!_token) {
  window.location = `${authEndpoint}?client_id=${clientId}&redirect_uri=${redirectUri}&scope=${scopes.join('%20')}&response_type=token&show_dialog=true`;
}
/*function show_image(src, width, height, alt) {
  var img = document.createElement("img");
  img.src = src;
  img.width = width;
  img.height = height;
  img.alt = alt;
  document.body.appendChild(img);
}*/
// function readTextFile(file)
// {
//     var rawFile = new XMLHttpRequest();
//     rawFile.open("GET", file, false);
//     rawFile.onreadystatechange = function ()
//     {
//         if(rawFile.readyState === 4)
//         {
//             if(rawFile.status === 200 || rawFile.status == 0)
//             {
//                 var allText = rawFile.responseText;
//                 alert(allText);
//             }
//         }
//     }
//     document.getElementById("main_img").src = allText;
//     rawFile.send(null);
// }
document.getElementById('file-picker').addEventListener('change', function(event) {
  event.preventDefault();
  let formData = new FormData();
  let image = document.getElementById('file-picker').files[0];
  formData.append("file", image);
  formData.append("token", _token);
  // image.url = image.replace("http","https");
  
  console.log("url of image");
  console.log(image.name);
  console.log("it is working!");
  
  var request = new XMLHttpRequest();
  request.open("POST", document.getElementById('upload-form').action);
  request.send(formData);
  document.body.style.backgroundColor = "#6ae368"
  console.log(event);
  console.log('before');
  setTimeout(function(){
    console.log('after');
  },1000);
  var newImg = "/app/images/";
  console.log(newImg.concat(image.name));
  
  document.getElementById("main_img").src = "/getimage";
  // readTextFile('/app/public/imagedataFile.txt')
});