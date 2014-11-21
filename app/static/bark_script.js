$(document).ready(function(){
	// set page name to a variable
	var pageName = location.pathname.split('/').slice(-1)[0];
	
	if (pageName = 'index') {
		// event if text is entered into the bark field
		$('#barkBody').keyup(function(){
			$goodLength = $("<p class='valid'>" + (140 - $('#barkBody').val().length) + "</p>")
			$overLength = $("<p class='invalid'>" + (140 - $('#barkBody').val().length) + "</p>")
		
			// Display characters remaining in green if over 0
			if ($('#barkBody').val().length < 141){
 				$('#barkCount').html($goodLength);
 				$('#barkSubmit').show();
 			}
 			// If a user enters over 140 characters, the Bark button will disappear
			// and the text will turn red
 			else {
 				$('#barkCount').html($overLength);
 				$('#barkSubmit').hide();
 			};
		});
	} // end if statement to check page name
});
