function togglePassword(fieldId, toggleId) {
  const field  = document.getElementById(fieldId);
  const toggle = document.getElementById(toggleId).querySelector("img");

  if (field.type === "password") {
    field.type = "text";
    toggle.src = "/static/hide.png";
    toggle.alt = "Hide Password";
  } else {
    field.type = "password";
    toggle.src = "/static/eye.png";
    toggle.alt = "Show Password";
  }
}

function copyURL() {
    var copyText = document.getElementById("shareURL");
    copyText.select();
    copyText.setSelectionRange(0, 99999);
    document.execCommand("copy");
    alert("Copied the URL: " + copyText.value);
  }
  
function shareWithFriend() {

  var friend = prompt("Enter your friend's username:");
  if (friend && friend.trim() !== "") {
    fetch("/check_user/" + encodeURIComponent(friend))
      .then(response => response.json())
      .then(data => {
        if (data.exists) {

          alert("Shared playlist link with " + friend + ":\n" + document.getElementById("shareURL").value);
        } else {
            
          var errorMsg = document.getElementById("errorMsg");
          errorMsg.textContent = "Username not found, try again!";
          errorMsg.style.display = "block";
          setTimeout(function() {
            errorMsg.style.display = "none";
          }, 3000);
        }
      })
      .catch(error => {
        console.error("Error checking user:", error);
        var errorMsg = document.getElementById("errorMsg");
        errorMsg.textContent = "An error occurred, please try again.";
        errorMsg.style.display = "block";
        setTimeout(function() {
          errorMsg.style.display = "none";
        }, 3000);
      });
  } else {
    alert("No friend's username entered. Please try again.");
  }
}

var deleteUrl = "";
function showDeleteMiniwindow(playlistName, url) {
  deleteUrl = url; 
  document.getElementById("MiniwindowText").textContent = "Are you sure you want to delete the playlist '" + playlistName + "'?";
  document.getElementById("deleteConfirm").style.display = "block";
}
  
function closeConfirm() {
  document.getElementById("deleteConfirm").style.display = "none";
}
  
function noDeletion() {
  document.getElementById("deleteConfirm").style.display = "none";
}
  
function confirmDeletion() {
  window.location.href = deleteUrl;
}
  
setTimeout(function(){
  var notif = document.getElementById("notification");
  if (notif) {
    notif.style.display = "none";
  }
}, 3000);
  

document.addEventListener('play', function(e) {
  const audios = document.getElementsByTagName('audio');
  for (let i = 0; i < audios.length; i++) {
    if (audios[i] !== e.target) {
      audios[i].pause();
    }
  }
}, true);

document.addEventListener('DOMContentLoaded', function() {
  const audioElements = Array.from(document.querySelectorAll('audio'));

  audioElements.forEach((audio, index) => {
    audio.addEventListener('ended', () => {
  
      const nextAudio = audioElements[index + 1];
      if (nextAudio) {
        nextAudio.play();
      } else {
        alert("No more songs in the playlist.");
      }
    });
  });
});

  
function copyURL() {
  var copyText = document.getElementById("shareURL");
  copyText.select();
  copyText.setSelectionRange(0, 99999);
  document.execCommand("copy");
    lert("Copied the URL: " + copyText.value);
}

function openMiniwindow() { 
  document.getElementById("friendMiniwindow").style.display = "block"; 
  document.getElementById("miniwindowError").innerText = ""; 
  document.getElementById("friendInput").value = "";
}
  
function closeMiniwindow() {
  document.getElementById("friendMiniwindow").style.display = "none"; 
}
  
function submitFriend() {
  var friendUsername = document.getElementById("friendInput").value.trim();
  if (!friendUsername) {
    document.getElementById("miniwindowError").innerText = "Please enter a username.";
    return;
  }
  fetch(`/check_user/${friendUsername}`)
    .then(response => response.json())
    .then(data => {
      if (data.exists) {
        let currentUrl = new URL(document.getElementById("shareURL").value);
        const pathParts = currentUrl.pathname.split("/");
        
        // If sharing an artist
        if (pathParts.includes("share_artist")) {
          const username = pathParts[2];
          const artist = pathParts[3];
          const newUrl = `/share_artist/${username}/${encodeURIComponent(artist)}?friend_username=${encodeURIComponent(friendUsername)}`;
          window.location.href = newUrl;
        }
        // If sharing a song
        else if (pathParts.includes("share_song")) {
          const songId = pathParts[2];  // share_song/<song_id>
          const newUrl = `/share_song/${songId}?friend_username=${encodeURIComponent(friendUsername)}`;
          window.location.href = newUrl;
        }
        // If sharing a genre
        else if (pathParts.includes("share_genre")) {
          const username = pathParts[2];
          const genre = pathParts[3];
          const newUrl = `/share_genre/${username}/${encodeURIComponent(genre)}?friend_username=${encodeURIComponent(friendUsername)}`;
          window.location.href = newUrl;
        }
        // Fallback for other routes
        else {
          currentUrl.searchParams.set("friend_username", friendUsername);
          window.location.href = currentUrl.toString();
        }
      } else {
        document.getElementById("miniwindowError").innerText = "Username not found, try again.";
      }
    })
    .catch(error => {
      console.error('Error checking friend username:', error);
      document.getElementById("miniwindowError").innerText = "An error occurred, please try again.";
    });
}


  

function copyURL() {
  var shareInput = document.getElementById("shareURL");
  shareInput.select();
  
  navigator.clipboard.writeText(shareInput.value).then(() => {
    alert("URL copied to clipboard!");
  }).catch(err => {
    console.error("Failed to copy URL:", err);
    alert("Failed to copy URL");
  });
}
  
window.onclick = function(event) {
  var miniWindow = document.getElementById("friendMiniwindow");
  if (event.target == miniWindow) { 
    closeMiniwindow(); 
  }
}
  
function copyURL(elementId) {
  var copyText = document.getElementById(elementId);
  copyText.select();
  document.execCommand("copy");
  alert("Copied the URL: " + copyText.value);
}

function copyURL(id = "shareURL") {
  const input = document.getElementById(id);
  if (!input) {
    console.error("copyURL: element not found:", id);
    alert("Unable to find URL to copy.");
    return;
  }
  input.select();
  navigator.clipboard.writeText(input.value)
    .then(() => alert("Copied the URL: " + input.value))
    .catch(err => {
      console.error("copyURL failed:", err);
      alert("Failed to copy URL.");
    });
}
