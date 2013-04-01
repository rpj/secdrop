var gExpected = -1;
var gProcessed = -1;
var gSuccess = -1;
var gFailed = -1;

  function encFullFile(file, pass) {
    var reader = new FileReader();
    reader.onload = function(e) {
      var enced = CryptoJS.AES.encrypt(e.target.result, pass);
      gProcessed++;
      progress();
      var encstr = "" + enced;

      $('#status').append("Sending encrypted <i>" + file.name + "</i>...<br/>");

      $.ajax({
        url: '/sec.cgi',
        type: 'POST',
        data: encstr,
        processData: false,
        contentType: false
      }).done(function(d) {
        gProcessed++;
        if (d.result) { 
          gSuccess++;
          $('#status').append("Successfully sent <i>" + file.name + "</i><br/>");
        } else {
          gFailed++;
          $('#status').append("Failed to send <i>" + file.name + "</i><br/>");
        }
        progress();
      }).fail(function(d) { 
        gProcessed++;
        gFailed++;
        $('#status').append("Server error sending <i>" + file.name + "</i><br/>");
        progress();
      });
    };

    reader.readAsDataURL(file);
  } 

  function handleFiles() {
    var files = document.getElementById('files').files;
    var pass = document.getElementById('pass').value;

    gProcessed = gSuccess = gFailed = 0;
    gExpected = files.length * 2;    
    
    $('#result').show();
    progress();

    for (var i = 0, file; file = files[i]; i++) {
      $('#status').append("Putting <i>" + file.name + "</i> into the vault...<br/>");
      encFullFile(file, pass);
    }
  }
  
  function progress() {
    if (gProcessed) {

        if (gProcessed == gExpected) {
          $('#result').text("Done! " + (gFailed ? (gFailed + " file(s) failed to send.") : ""));

          $('#clicky').button('reset');
          $('#pass').removeAttr('disabled');
          $('#files').removeAttr('disabled');
        }
        else {
          $('#progress').width('' + ((gProcessed / gExpected) * 100) + '%');
        } 
    }
  }

  function clicky() {
    if (!document.getElementById('pass').value) {
      alert("You must provide a password!");
    }
    else if (!document.getElementById('files').files[0]) {
      alert("You didn't specify any files!");
    }
    else {
      $('#clicky').button('loading');
      $('#pass').attr('disabled', 'disabled');
      $('#files').attr('disabled', 'disabled');

      $('#scon').show();
      handleFiles();
    }
  }

